from arcaea_offline.database.models.v4.songs import (
    Chart,
    ChartInfo,
    Difficulty,
    Pack,
    Song,
    SongsBase,
    SongsViewBase,
)


def _song(**kw):
    defaults = {"artist": "test"}
    defaults.update(kw)
    return Song(**defaults)


def _difficulty(**kw):
    defaults = {"rating_plus": False, "audio_override": False, "jacket_override": False}
    defaults.update(kw)
    return Difficulty(**defaults)


class Test_Chart:
    def init_db(self, session):
        SongsBase.metadata.create_all(session.bind, checkfirst=False)
        SongsViewBase.metadata.create_all(session.bind, checkfirst=False)

    def test_chart_info(self, db_session):
        self.init_db(db_session)

        pre_entites = [
            Pack(id="test", name="Test Pack"),
            _song(idx=0, id="song0", set="test", title="Full Chart Info"),
            _song(idx=1, id="song1", set="test", title="Partial Chart Info"),
            _song(idx=2, id="song2", set="test", title="No Chart Info"),
            _difficulty(song_id="song0", rating_class=2, rating=9),
            _difficulty(song_id="song1", rating_class=2, rating=9),
            _difficulty(song_id="song2", rating_class=2, rating=9),
            ChartInfo(song_id="song0", rating_class=2, constant=90, notes=1234),
            ChartInfo(song_id="song1", rating_class=2, constant=90),
        ]

        db_session.add_all(pre_entites)
        db_session.commit()

        chart_song0_ratingclass2 = (
            db_session.query(Chart)
            .where((Chart.song_id == "song0") & (Chart.rating_class == 2))
            .one()
        )

        assert chart_song0_ratingclass2.constant == 90
        assert chart_song0_ratingclass2.notes == 1234

        chart_song1_ratingclass2 = (
            db_session.query(Chart)
            .where((Chart.song_id == "song1") & (Chart.rating_class == 2))
            .one()
        )

        assert chart_song1_ratingclass2.constant == 90
        assert chart_song1_ratingclass2.notes is None

        chart_song2_ratingclass2 = (
            db_session.query(Chart)
            .where((Chart.song_id == "song2") & (Chart.rating_class == 2))
            .first()
        )

        assert chart_song2_ratingclass2 is None

    def test_difficulty_title_override(self, db_session):
        self.init_db(db_session)

        pre_entites = [
            Pack(id="test", name="Test Pack"),
            _song(idx=0, id="test", set="test", title="Test"),
            _difficulty(song_id="test", rating_class=0, rating=2),
            _difficulty(song_id="test", rating_class=1, rating=5),
            _difficulty(song_id="test", rating_class=2, rating=8),
            _difficulty(
                song_id="test", rating_class=3, rating=10, title="TEST ~REVIVE~"
            ),
            ChartInfo(song_id="test", rating_class=0, constant=10),
            ChartInfo(song_id="test", rating_class=1, constant=10),
            ChartInfo(song_id="test", rating_class=2, constant=10),
            ChartInfo(song_id="test", rating_class=3, constant=10),
        ]

        db_session.add_all(pre_entites)
        db_session.commit()

        charts_original_title = (
            db_session.query(Chart)
            .where((Chart.song_id == "test") & (Chart.rating_class in [0, 1, 2]))
            .all()
        )

        assert all(chart.title == "Test" for chart in charts_original_title)

        chart_overrided_title = (
            db_session.query(Chart)
            .where((Chart.song_id == "test") & (Chart.rating_class == 3))
            .one()
        )

        assert chart_overrided_title.title == "TEST ~REVIVE~"
