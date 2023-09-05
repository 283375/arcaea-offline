import logging
from typing import Iterable, List, Optional, Type, Union

from sqlalchemy import Engine, func, inspect, select
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, sessionmaker

from .external.arcsong.arcsong_json import ArcSongJsonBuilder
from .external.exports import ScoreExport, exporters
from .models.config import *
from .models.scores import *
from .models.songs import *
from .singleton import Singleton

logger = logging.getLogger(__name__)


class Database(metaclass=Singleton):
    def __init__(self, engine: Optional[Engine]):
        try:
            self.__engine
        except AttributeError:
            self.__engine = None

        if engine is None:
            if isinstance(self.engine, Engine):
                return
            raise ValueError("No sqlalchemy.Engine instance specified before.")
        elif isinstance(engine, Engine):
            if isinstance(self.engine, Engine):
                logger.warning(
                    f"A sqlalchemy.Engine instance {self.engine} has been specified "
                    f"and will be replaced to {engine}"
                )
            self.engine = engine
        else:
            raise ValueError(
                f"A sqlalchemy.Engine instance expected, not {repr(engine)}"
            )

    @property
    def engine(self) -> Engine:
        return self.__engine  # type: ignore

    @engine.setter
    def engine(self, value: Engine):
        if not isinstance(value, Engine):
            raise ValueError("Database.engine only accepts sqlalchemy.Engine")
        self.__engine = value
        self.__sessionmaker = sessionmaker(self.__engine)

    @property
    def sessionmaker(self):
        return self.__sessionmaker

    # region init

    def init(self, checkfirst: bool = True):
        # create tables & views
        if checkfirst:
            # > https://github.com/kvesteri/sqlalchemy-utils/issues/396
            # > view.create_view() causes DuplicateTableError on Base.metadata.create_all(checkfirst=True)
            # so if `checkfirst` is True, drop these views before creating
            SongsViewBase.metadata.drop_all(self.engine)
            ScoresViewBase.metadata.drop_all(self.engine)

        SongsBase.metadata.create_all(self.engine, checkfirst=checkfirst)
        SongsViewBase.metadata.create_all(self.engine)
        ScoresBase.metadata.create_all(self.engine, checkfirst=checkfirst)
        ScoresViewBase.metadata.create_all(self.engine)
        ConfigBase.metadata.create_all(self.engine, checkfirst=checkfirst)

        # insert version property
        with self.sessionmaker() as session:
            stmt = select(Property.value).where(Property.key == "version")
            result = session.execute(stmt).fetchone()
            if not checkfirst or not result:
                session.add(Property(key="version", value="4"))
                session.commit()

    def check_init(self) -> bool:
        # check table exists
        expect_tables = (
            list(SongsBase.metadata.tables.keys())
            + list(ScoresBase.metadata.tables.keys())
            + list(ConfigBase.metadata.tables.keys())
            + [
                Chart.__tablename__,
                ScoreCalculated.__tablename__,
                ScoreBest.__tablename__,
                CalculatedPotential.__tablename__,
            ]
        )
        return all(inspect(self.engine).has_table(t) for t in expect_tables)

    # endregion

    def version(self) -> Union[int, None]:
        stmt = select(Property).where(Property.key == "version")
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return None if result is None else int(result.value)

    # region Pack

    def get_packs(self):
        stmt = select(Pack)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_pack(self, pack_id: str):
        stmt = select(Pack).where(Pack.id == pack_id)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    def get_pack_localized(self, pack_id: str):
        stmt = select(PackLocalized).where(PackLocalized.id == pack_id)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    # endregion

    # region Song

    def get_songs(self):
        stmt = select(Song)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_song(self, song_id: str):
        stmt = select(Song).where(Song.id == song_id)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    def get_song_localized(self, song_id: str):
        stmt = select(SongLocalized).where(SongLocalized.id == song_id)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    # endregion

    # region Difficulty

    def get_difficulties(self):
        stmt = select(Difficulty)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_difficulties_by_song_id(self, song_id: str):
        stmt = select(Difficulty).where(Difficulty.song_id == song_id)
        with self.sessionmaker() as session:
            results = session.scalars(stmt)
        return results

    def get_difficulties_localized_by_song_id(self, song_id: str):
        stmt = select(DifficultyLocalized).where(DifficultyLocalized.song_id == song_id)
        with self.sessionmaker() as session:
            results = session.scalars(stmt)
        return results

    def get_difficulty(self, song_id: str, rating_class: int):
        stmt = select(Difficulty).where(
            (Difficulty.song_id == song_id) & (Difficulty.rating_class == rating_class)
        )
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    def get_difficulty_localized(self, song_id: str, rating_class: int):
        stmt = select(DifficultyLocalized).where(
            (DifficultyLocalized.song_id == song_id)
            & (DifficultyLocalized.rating_class == rating_class)
        )
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    # endregion

    # region ChartInfo

    def get_chart_infos(self):
        stmt = select(ChartInfo)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_chart_infos_by_song_id(self, song_id: str):
        stmt = select(ChartInfo).where(ChartInfo.song_id == song_id)
        with self.sessionmaker() as session:
            results = session.scalars(stmt)
        return results

    def get_chart_info(self, song_id: str, rating_class: int):
        stmt = select(ChartInfo).where(
            (ChartInfo.song_id == song_id) & (ChartInfo.rating_class == rating_class)
        )
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    # endregion

    # region Chart

    def get_charts_by_pack_id(self, pack_id: str):
        stmt = select(Chart).where(Chart.set == pack_id)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_charts_by_song_id(self, song_id: str):
        stmt = select(Chart).where(Chart.song_id == song_id)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_chart(self, song_id: str, rating_class: int):
        stmt = select(Chart).where(
            (Chart.song_id == song_id) & (Chart.rating_class == rating_class)
        )
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    # endregion

    # region Score

    def get_scores(self):
        stmt = select(Score)
        with self.sessionmaker() as session:
            results = list(session.scalars(stmt))
        return results

    def get_score(self, score_id: int):
        stmt = select(Score).where(Score.id == score_id)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    def insert_score(self, score: Score):
        with self.sessionmaker() as session:
            session.add(score)
            session.commit()

    def insert_scores(self, scores: Iterable[Score]):
        with self.sessionmaker() as session:
            session.add_all(scores)
            session.commit()

    def update_score(self, score: Score):
        if score.id is None:
            raise ValueError(
                "Cannot determine which score to update, please specify `score.id`"
            )
        with self.sessionmaker() as session:
            session.merge(score)
            session.commit()

    def delete_score(self, score: Score):
        with self.sessionmaker() as session:
            session.delete(score)
            session.commit()

    # endregion

    def get_b30(self):
        stmt = select(CalculatedPotential.b30).select_from(CalculatedPotential)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result

    # region COUNT

    def __count_table(self, base: Type[DeclarativeBase]):
        stmt = select(func.count()).select_from(base)
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result or 0

    def __count_column(self, column: InstrumentedAttribute):
        stmt = select(func.count(column))
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result or 0

    def count_packs(self):
        return self.__count_column(Pack.id)

    def count_songs(self):
        return self.__count_column(Song.id)

    def count_difficulties(self):
        return self.__count_table(Difficulty)

    def count_chart_infos(self):
        return self.__count_table(ChartInfo)

    def count_complete_chart_infos(self):
        stmt = (
            select(func.count())
            .select_from(ChartInfo)
            .where((ChartInfo.constant != None) & (ChartInfo.notes != None))
        )
        with self.sessionmaker() as session:
            result = session.scalar(stmt)
        return result or 0

    def count_charts(self):
        return self.__count_table(Chart)

    def count_scores(self):
        return self.__count_column(Score.id)

    def count_scores_calculated(self):
        return self.__count_table(ScoreCalculated)

    def count_scores_best(self):
        return self.__count_table(ScoreBest)

    # endregion

    # region export

    def export_scores(self) -> List[ScoreExport]:
        scores = self.get_scores()
        return [exporters.score(score) for score in scores]

    def generate_arcsong(self):
        with self.sessionmaker() as session:
            arcsong = ArcSongJsonBuilder(session).generate_arcsong_json()
        return arcsong

    # endregion
