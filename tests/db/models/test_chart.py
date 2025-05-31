"""
Database models v5

Chart functionalities
- basic data handling
- Difficulty song info overriding
"""

from datetime import datetime, timezone

from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models import (
    Chart,
    ChartInfo,
    Difficulty,
    ModelBase,
    ModelViewBase,
    Pack,
    Song,
)


class TestChart:
    def init_db(self, session):
        ModelBase.metadata.create_all(session.bind)
        ModelViewBase.metadata.create_all(session.bind)

    def test_basic(self, db_session):
        self.init_db(db_session)

        pack_id = "test_pack"
        song_id = "test_song"
        rating_class = ArcaeaRatingClass.FUTURE

        pack = Pack(id=pack_id, name="Test Pack")
        song = Song(
            idx=2,
            id=song_id,
            title="~TEST~",
            artist="~test~",
            pack_id=pack_id,
            added_at=datetime(2024, 7, 4, tzinfo=timezone.utc),
        )
        difficulty = Difficulty(
            song_id=song_id,
            rating_class=rating_class,
            rating=9,
            is_rating_plus=True,
        )
        chart_info = ChartInfo(
            song_id=song_id,
            rating_class=rating_class,
            constant=98,
            notes=980,
            added_at=datetime(2024, 7, 12, tzinfo=timezone.utc),
        )
        db_session.add_all([pack, song, difficulty, chart_info])
        db_session.commit()

        chart: Chart = (
            db_session.query(Chart)
            .where((Chart.song_id == song_id) & (Chart.rating_class == rating_class))
            .one()
        )

        # `song_id` and `rating_class` are guarded by the WHERE clause above
        assert chart.song_idx == song.idx
        assert chart.title == song.title
        assert chart.artist == song.artist
        assert chart.pack_id == song.pack_id
        assert chart.rating == difficulty.rating
        assert chart.is_rating_plus == difficulty.is_rating_plus
        assert chart.constant == chart_info.constant
        assert chart.notes == chart_info.notes

    def test_difficulty_override(self, db_session):
        self.init_db(db_session)

        pack_id = "test_pack"
        song_id = "test_song"
        rating_class = ArcaeaRatingClass.FUTURE

        pack = Pack(id=pack_id, name="Test Pack")
        song = Song(
            idx=2,
            id=song_id,
            title="~TEST~",
            artist="~test~",
            pack_id=pack_id,
            added_at=datetime(2024, 7, 4, tzinfo=timezone.utc),
        )
        difficulty = Difficulty(
            song_id=song_id,
            rating_class=rating_class,
            rating=9,
            is_rating_plus=True,
            title="~TEST DIFF~",
            artist="~diff~",
        )
        chart_info = ChartInfo(
            song_id=song_id,
            rating_class=rating_class,
            constant=98,
            notes=980,
            added_at=datetime(2024, 7, 12, tzinfo=timezone.utc),
        )
        db_session.add_all([pack, song, difficulty, chart_info])
        db_session.commit()

        chart: Chart = (
            db_session.query(Chart)
            .where((Chart.song_id == song_id) & (Chart.rating_class == rating_class))
            .one()
        )

        assert chart.song_idx == song.idx
        assert chart.title == difficulty.title
        assert chart.artist == difficulty.artist
