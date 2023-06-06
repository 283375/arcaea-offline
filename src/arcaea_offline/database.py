import os
import sqlite3
from dataclasses import fields, is_dataclass
from typing import List, NamedTuple, Optional, TypeVar, Union

from thefuzz import fuzz
from thefuzz import process as fuzz_process

from .models import DbAliasRow, DbCalculatedRow, DbChartRow, DbPackageRow, DbScoreRow
from .utils.singleton import Singleton
from .utils.types import TDataclass

T = TypeVar("T", bound=TDataclass)


class Database(metaclass=Singleton):
    dbDir = os.getcwd()
    dbFilename = "arcaea_offline.db"

    def __init__(self):
        self.__conn = sqlite3.connect(os.path.join(self.dbDir, self.dbFilename))
        self.__conn.execute("PRAGMA journal_mode = WAL;")
        self.__conn.execute("PRAGMA foreign_keys = ON;")

    @property
    def conn(self):
        return self.__conn

    def validate_song_id(self, song_id):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM charts WHERE song_id = ?", (song_id,))
            result = cursor.fetchone()
            return result[0] > 0

    def update_arcsong_db(self, path: Union[str, bytes]):
        with sqlite3.connect(path) as arcsong_conn:
            arcsong_cursor = arcsong_conn.cursor()
            data = {
                "charts": arcsong_cursor.execute(
                    "SELECT song_id, rating_class, name_en, name_jp, artist, bpm, bpm_base, 'set', time, side, world_unlock, remote_download, bg, date, version, difficulty, rating, note, chart_designer, jacket_designer, jacket_override, audio_override FROM charts"
                ).fetchall(),
                "aliases": arcsong_cursor.execute(
                    "SELECT sid, alias FROM alias"
                ).fetchall(),
                "packages": arcsong_cursor.execute(
                    "SELECT id, name FROM packages"
                ).fetchall(),
            }

        with self.conn as conn:
            cursor = conn.cursor()
            for table, rows in data.items():
                columns = [
                    row[0]
                    for row in cursor.execute(
                        f"SELECT * FROM {table} LIMIT 1"
                    ).description
                ]
                column_count = len(columns)
                assert column_count == len(
                    rows[0]
                ), f"Incompatible column count for table '{table}'"
                placeholders = ", ".join(["?" for _ in range(column_count)])
                update_clauses = ", ".join(
                    [f"{column} = excluded.{column}" for column in columns]
                )
                cursor.executemany(
                    f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO UPDATE SET {update_clauses}",
                    rows,
                )
            conn.commit()

    def init(self):
        create_sqls = [
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
                pure               INTEGER NOT NULL,
                far                INTEGER NOT NULL,
                lost               INTEGER NOT NULL,
                time               INTEGER NOT NULL,
                max_recall         INTEGER,

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
                scores.song_id,
                scores.rating_class,
                scores.score,
                scores.pure,
                scores.far,
                scores.lost,
                scores.time,
                charts.rating,
                charts.note,
                CAST ( ROUND( score - ( pure * 10000000 / note ) - ( far * 0.5 * 10000000 / note ) ) AS INTEGER ) AS pure_small,
                CASE
                    WHEN score >= 10000000 THEN
                    rating / 10.0 + 2 
                    WHEN score >= 9800000 THEN
                    rating / 10.0 + 1 + ( score - 9800000 ) / 200000.0 ELSE MAX( rating / 10.0, 0 ) + ( score - 9500000 ) / 300000.0 
                END AS potential 
            FROM
                scores
                LEFT JOIN charts ON scores.rating_class = charts.rating_class 
                AND scores.song_id = charts.song_id 
            GROUP BY
                scores.song_id,
                scores.rating_class
            """,
            """
            CREATE VIEW IF NOT EXISTS recent_10 AS
            SELECT
                c.song_id,
                c.rating_class,
                MAX(c.potential) AS potential
            FROM
                calculated c
            WHERE
                c.time IN (
                    SELECT DISTINCT time
                    FROM calculated
                    ORDER BY time DESC
                    LIMIT 10
                )
            GROUP BY
                c.song_id,
                c.rating_class
            """,
            """
            CREATE VIEW IF NOT EXISTS best_30 AS
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
            LIMIT 30
            """,
            """
            CREATE VIEW IF NOT EXISTS calculated_potential AS
            SELECT
                r10_avg AS r10,
                b30_avg AS b30,
                (r10_sum + b30_sum) / (r10_count + b30_count) AS potential
            FROM
                (SELECT SUM(potential) AS r10_sum, AVG(potential) AS r10_avg, COUNT(*) AS r10_count FROM recent_10) r10,
                (SELECT SUM(potential) AS b30_sum, AVG(potential) AS b30_avg, COUNT(*) AS b30_count FROM best_30) b30
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
        ]

        with self.conn as conn:
            cursor = conn.cursor()
            for sql in create_sqls:
                cursor.execute(sql)
            conn.commit()

    def __get_columns_from_dataclass(self, dataclass) -> List[str]:
        if is_dataclass(dataclass):
            dc_fields = fields(dataclass)
            return [field.name for field in dc_fields]
        return []

    def __get_columns_clause(self, columns: List[str]):
        return ", ".join([f'"{column}"' for column in columns])

    def __get_table(
        self, table_name: str, datacls: T, where_clause: str = "", params=None
    ) -> List[T]:
        if params is None:
            params = []
        columns_clause = self.__get_columns_clause(
            self.__get_columns_from_dataclass(datacls)
        )

        sql = f"SELECT {columns_clause} FROM {table_name}"
        if where_clause:
            sql += " WHERE "
            sql += where_clause
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return [datacls(*row) for row in cursor.fetchall()]

    def get_packages(self):
        return self.__get_table("packages", DbPackageRow)

    def get_aliases(self):
        return self.__get_table("aliases", DbAliasRow)

    def get_aliases_by_song_id(self, song_id: str):
        return self.__get_table("aliases", DbAliasRow, "song_id = ?", (song_id,))

    def get_charts(self):
        return self.__get_table("charts", DbChartRow)

    def get_charts_by_song_id(self, song_id: str):
        return self.__get_table("charts", DbChartRow, "song_id = ?", (song_id,))

    def get_charts_by_package_id(self, package_id: str):
        return self.__get_table("charts", DbChartRow, "package_id = ?", (package_id,))

    class FuzzySearchSongIdResult(NamedTuple):
        song_id: str
        confidence: int

    def fuzzy_search_song_id(
        self, input_str: str, limit: int = 5
    ) -> List[FuzzySearchSongIdResult]:
        with self.conn as conn:
            cursor = conn.cursor()
            db_results = cursor.execute(
                "SELECT song_id, name FROM song_id_names"
            ).fetchall()
        name_song_id_map = {r[1]: r[0] for r in db_results}
        names = name_song_id_map.keys()
        fuzzy_results = fuzz_process.extractBests(input_str, names, scorer=fuzz.partial_ratio, limit=limit)  # type: ignore
        results = {}
        for fuzzy_result in fuzzy_results:
            name = fuzzy_result[0]
            confidence = fuzzy_result[1]
            song_id = name_song_id_map[name]
            results[song_id] = max(confidence, results.get(song_id, 0))

        return [
            self.FuzzySearchSongIdResult(si, confi) for si, confi in results.items()
        ]

    def get_scores(
        self,
        *,
        song_id: Optional[List[str]] = None,
        rating_class: Optional[List[int]] = None,
    ):
        where_clauses = []
        params = []
        if song_id:
            where_clauses.append(f"song_id IN ({','.join('?'*len(song_id))})")
            params.extend(song_id)
        if rating_class:
            where_clauses.append(f"rating_class IN ({','.join('?'*len(rating_class))})")
            params.extend(rating_class)

        return self.__get_table(
            "scores", DbScoreRow, " AND ".join(where_clauses), params
        )

    def get_calculated(
        self,
        *,
        song_id: Optional[List[str]] = None,
        rating_class: Optional[List[int]] = None,
    ):
        where_clauses = []
        params = []
        if song_id:
            where_clauses.append(f"song_id IN ({','.join('?'*len(song_id))})")
            params.extend(song_id)
        if rating_class:
            where_clauses.append(f"rating_class IN ({','.join('?'*len(rating_class))})")
            params.extend(rating_class)

        return self.__get_table(
            "calculated", DbCalculatedRow, " AND ".join(where_clauses), params
        )

    def get_b30(self) -> float:
        with self.conn as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT b30 FROM calculated_potential").fetchone()[0]

    def get_r10(self) -> float:
        with self.conn as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT r10 FROM calculated_potential").fetchone()[0]

    def get_potential(self) -> float:
        with self.conn as conn:
            cursor = conn.cursor()
            return cursor.execute(
                "SELECT potential FROM calculated_potential"
            ).fetchone()[0]

    def insert_score(self, score: DbScoreRow):
        columns = self.__get_columns_from_dataclass(DbScoreRow)
        columns_clause = self.__get_columns_clause(columns)
        params = [getattr(score, column) for column in columns]
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO scores({columns_clause}) VALUES ({', '.join('?' * len(params))})",
                params,
            )
            conn.commit()
