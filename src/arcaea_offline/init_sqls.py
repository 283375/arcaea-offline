from typing import Dict, List, TypedDict


class VersionSqls(TypedDict):
    init: List[str]
    update: List[str]


INIT_SQLS: Dict[int, VersionSqls] = {
    1: {
        "init": [
            # region CREATE
            """
            CREATE TABLE IF NOT EXISTS charts (
                song_id          TEXT    NOT NULL,
                rating_class     INTEGER NOT NULL,
                name_en          TEXT    NOT NULL,
                name_jp          TEXT,
                artist           TEXT    NOT NULL,
                bpm              TEXT    NOT NULL,
                bpm_base         REAL    NOT NULL,
                package_id       TEXT    NOT NULL,
                time             INTEGER,
                side             INTEGER NOT NULL,
                world_unlock     BOOLEAN NOT NULL,
                remote_download  BOOLEAN,
                bg               TEXT    NOT NULL,
                date             INTEGER NOT NULL,
                version          TEXT    NOT NULL,
                difficulty       INTEGER NOT NULL,
                rating           INTEGER NOT NULL,
                note             INTEGER NOT NULL,
                chart_designer   TEXT,
                jacket_designer  TEXT,
                jacket_override  BOOLEAN NOT NULL,
                audio_override   BOOLEAN NOT NULL,

                PRIMARY KEY (song_id, rating_class)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS aliases (
                song_id  TEXT NOT NULL,
                alias    TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS packages (
                package_id  TEXT NOT NULL,
                name        TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scores (
                id                 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                song_id            TEXT NOT NULL,
                rating_class       INTEGER NOT NULL,
                score              INTEGER NOT NULL,
                pure               INTEGER,
                far                INTEGER,
                lost               INTEGER,
                time               INTEGER NOT NULL,
                max_recall         INTEGER,
                clear_type         INTEGER,

                FOREIGN KEY (song_id, rating_class) REFERENCES charts(song_id, rating_class) ON UPDATE CASCADE ON DELETE NO ACTION
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS properties (
                key    TEXT NOT NULL UNIQUE,
                value  TEXT NOT NULL
            )
            """,
            """
            CREATE VIEW IF NOT EXISTS calculated AS
            SELECT
                scores.id,
                scores.song_id,
                scores.rating_class,
                scores.score,
                scores.pure,
                scores.far,
                scores.lost,
                scores.time,
                charts.rating,
                charts.note,
                score - FLOOR(( pure * 10000000.0 / note ) + ( far * 0.5 * 10000000.0 / note )) AS pure_small,
                CASE
                    WHEN score >= 10000000 THEN
                    rating / 10.0 + 2
                    WHEN score >= 9800000 THEN
                    rating / 10.0 + 1 + ( score - 9800000 ) / 200000.0
                    ELSE MAX(( rating / 10.0 ) + ( score - 9500000 ) / 300000.0, 0)
                END AS potential
            FROM
                scores
                LEFT JOIN charts ON scores.rating_class = charts.rating_class
                AND scores.song_id = charts.song_id
            GROUP BY
                scores.id
            """,
            """
            CREATE VIEW IF NOT EXISTS bests AS
            SELECT
                c.song_id,
                c.rating_class,
                MAX(c.potential) AS potential
            FROM
                calculated c
            GROUP BY
                c.song_id,
                c.rating_class
            ORDER BY
                potential DESC
            """,
            """
            CREATE VIEW IF NOT EXISTS calculated_potential AS
            SELECT
                b30_avg AS b30
            FROM
                ( SELECT AVG(potential) AS b30_avg FROM bests ORDER BY potential DESC LIMIT 30 )
            """,
            """
            CREATE VIEW IF NOT EXISTS song_id_names AS
            SELECT song_id, name
            FROM (
                SELECT song_id, alias AS name FROM aliases
                UNION ALL
                SELECT song_id, song_id AS name FROM charts
                UNION ALL
                SELECT song_id, name_en AS name FROM charts
                UNION ALL
                SELECT song_id, name_jp AS name FROM charts
            ) AS subquery
            WHERE name IS NOT NULL AND name <> ''
            GROUP BY song_id, name
            """,
            # endregion
            # region INSERT
            """
            INSERT INTO properties VALUES ('db_version', '1')
            """
            # endregion
        ],
        "update": [],
    }
}
