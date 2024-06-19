"""
Database model v5 common relationships

┌──────┐   ┌──────┐   ┌────────────┐   ┌────────────┐
│ Pack ◄───► Song ◄───► Difficulty ◄───┤ PlayResult │
└──────┘   └──┬───┘   └─────▲──────┘   └────────────┘
              │             │
              │       ┌─────▼─────┐
              └───────► ChartInfo │
                      └───────────┘
"""

from arcaea_offline.constants.enums import ArcaeaRatingClass
from arcaea_offline.database.models.v5 import (
    ChartInfo,
    Difficulty,
    ModelsV5Base,
    Pack,
    PlayResult,
    Song,
)


class TestSongRelationships:
    @staticmethod
    def init_db(session):
        ModelsV5Base.metadata.create_all(session.bind)

    def test_relationships(self, db_session):
        self.init_db(db_session)

        song_id = "test_song"
        title_en = "Test Lorem Ipsum"
        artist_en = "Test Artist"

        pack = Pack(
            id="test_pack",
            name="Test Pack",
            description="This is a test pack.",
        )

        song = Song(
            idx=1,
            id=song_id,
            title=title_en,
            artist=artist_en,
            pack_id=pack.id,
        )

        difficulty_pst = Difficulty(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.PAST,
            rating=2,
            rating_plus=False,
        )
        chart_info_pst = ChartInfo(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.PAST,
            constant=20,
            notes=200,
        )

        difficulty_prs = Difficulty(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.PRESENT,
            rating=7,
            rating_plus=True,
        )
        chart_info_prs = ChartInfo(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.PRESENT,
            constant=78,
            notes=780,
        )

        difficulty_ftr = Difficulty(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.FUTURE,
            rating=10,
            rating_plus=True,
        )
        chart_info_ftr = ChartInfo(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.FUTURE,
            constant=109,
            notes=1090,
        )

        difficulty_etr = Difficulty(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.ETERNAL,
            rating=9,
            rating_plus=True,
        )

        play_result_ftr = PlayResult(
            song_id=song.id,
            rating_class=ArcaeaRatingClass.FUTURE,
            score=123456,
        )

        db_session.add_all(
            [
                pack,
                song,
                difficulty_pst,
                chart_info_pst,
                difficulty_prs,
                chart_info_prs,
                difficulty_ftr,
                chart_info_ftr,
                difficulty_etr,
                play_result_ftr,
            ]
        )
        db_session.commit()

        assert pack.songs == [song]

        assert song.pack == pack
        assert song.difficulties == [
            difficulty_pst,
            difficulty_prs,
            difficulty_ftr,
            difficulty_etr,
        ]
        assert song.charts_info == [chart_info_pst, chart_info_prs, chart_info_ftr]

        assert difficulty_pst.song == song
        assert difficulty_prs.song == song
        assert difficulty_ftr.song == song
        assert difficulty_etr.song == song

        assert difficulty_pst.chart_info == chart_info_pst
        assert difficulty_prs.chart_info == chart_info_prs
        assert difficulty_ftr.chart_info == chart_info_ftr
        assert difficulty_etr.chart_info is None

        assert chart_info_pst.difficulty == difficulty_pst
        assert chart_info_prs.difficulty == difficulty_prs
        assert chart_info_ftr.difficulty == difficulty_ftr

        assert play_result_ftr.difficulty == difficulty_ftr
