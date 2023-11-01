from typing import List, Union

from sqlalchemy import select
from sqlalchemy.orm import Session
from whoosh.analysis import NgramFilter, StandardAnalyzer
from whoosh.fields import ID, KEYWORD, TEXT, Schema
from whoosh.filedb.filestore import RamStorage
from whoosh.qparser import FuzzyTermPlugin, MultifieldParser, OrGroup

from .models.songs import Song, SongLocalized
from .utils.search_title import recover_search_title


class Searcher:
    def __init__(self):
        self.text_analyzer = StandardAnalyzer() | NgramFilter(minsize=2, maxsize=5)
        self.song_schema = Schema(
            song_id=ID(stored=True, unique=True),
            title=TEXT(analyzer=self.text_analyzer, spelling=True),
            artist=TEXT(analyzer=self.text_analyzer, spelling=True),
            source=TEXT(analyzer=self.text_analyzer, spelling=True),
            keywords=KEYWORD(lowercase=True, stored=True, scorable=True),
        )
        self.storage = RamStorage()
        self.index = self.storage.create_index(self.song_schema)

        self.default_query_parser = MultifieldParser(
            ["song_id", "title", "artist", "source", "keywords"],
            self.song_schema,
            group=OrGroup,
        )
        self.default_query_parser.add_plugin(FuzzyTermPlugin())

    def import_songs(self, session: Session):
        writer = self.index.writer()
        songs = list(session.scalars(select(Song)))
        song_localize_stmt = select(SongLocalized)
        for song in songs:
            stmt = song_localize_stmt.where(SongLocalized.id == song.id)
            sl = session.scalar(stmt)
            song_id = song.id
            possible_titles: List[Union[str, None]] = [song.title]
            possible_artists: List[Union[str, None]] = [song.artist]
            possible_sources: List[Union[str, None]] = [song.source]
            if sl:
                possible_titles.extend(
                    [sl.title_ja, sl.title_ko, sl.title_zh_hans, sl.title_zh_hant]
                )
                possible_titles.extend(
                    recover_search_title(sl.search_title_ja)
                    + recover_search_title(sl.search_title_ko)
                    + recover_search_title(sl.search_title_zh_hans)
                    + recover_search_title(sl.search_title_zh_hant)
                )
                possible_artists.extend(
                    recover_search_title(sl.search_artist_ja)
                    + recover_search_title(sl.search_artist_ko)
                    + recover_search_title(sl.search_artist_zh_hans)
                    + recover_search_title(sl.search_artist_zh_hant)
                )
                possible_sources.extend(
                    [
                        sl.source_ja,
                        sl.source_ko,
                        sl.source_zh_hans,
                        sl.source_zh_hant,
                    ]
                )

            # remove empty items in list
            titles = [t for t in possible_titles if t != "" and t is not None]
            artists = [t for t in possible_artists if t != "" and t is not None]
            sources = [t for t in possible_sources if t != "" and t is not None]

            writer.update_document(
                song_id=song_id,
                title=" ".join(titles),
                artist=" ".join(artists),
                source=" ".join(sources),
                keywords=" ".join([song_id] + titles + artists + sources),
            )

        writer.commit()

    def did_you_mean(self, string: str):
        results = set()

        with self.index.searcher() as searcher:
            corrector_keywords = searcher.corrector("keywords")  # type: ignore
            corrector_song_id = searcher.corrector("song_id")  # type: ignore
            corrector_title = searcher.corrector("title")  # type: ignore
            corrector_artist = searcher.corrector("artist")  # type: ignore
            corrector_source = searcher.corrector("source")  # type: ignore

            results.update(corrector_keywords.suggest(string))
            results.update(corrector_song_id.suggest(string))
            results.update(corrector_title.suggest(string))
            results.update(corrector_artist.suggest(string))
            results.update(corrector_source.suggest(string))

        if string in results:
            results.remove(string)

        return list(results)

    def search(self, string: str, *, limit: int = 10):
        query_string = f"{string}"
        query = self.default_query_parser.parse(query_string)
        with self.index.searcher() as searcher:
            results = searcher.search(query, limit=limit)
            return [result.get("song_id") for result in results]
