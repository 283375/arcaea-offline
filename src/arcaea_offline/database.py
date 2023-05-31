import os
from .utils.singleton import Singleton
from .models import DbChartRow, DbPackageRow, DbScoreRow, DbCaculatedRow, DbAliasRow
import sqlite3
from typing import Union, List, Optional
from dataclasses import fields, is_dataclass


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
        with self.conn:
            result = self.conn.execute(
                "SELECT song_id FROM charts WHERE song_id = ?", (song_id,)
            ).fetchall()
            return len(result) > 0

    def update_arcsong_db(self, path: Union[str, bytes]):
        arcsong_conn = sqlite3.connect(path)
        data = {}
        with arcsong_conn:
            data["charts"] = arcsong_conn.execute(
                """
                SELECT song_id, rating_class, name_en, name_jp, artist, bpm, bpm_base, "set", time, side, world_unlock, remote_download, bg, date, version, difficulty, rating, note, chart_designer, jacket_designer, jacket_override, audio_override
                FROM charts
                """
            ).fetchall()
            data["aliases"] = arcsong_conn.execute(
                """
                SELECT sid, alias
                FROM alias
                """
            ).fetchall()
            data["packages"] = arcsong_conn.execute(
                """
                SELECT id, name
                FROM packages
                """
            ).fetchall()

        with self.conn as conn:
            for table in data:
                columns = [
                    row[0]
                    for row in conn.execute(
                        f"SELECT * FROM {table} LIMIT 1"
                    ).description
                ]
                column_count = len(columns)
                assert column_count == len(data[table][0])
                columns_insert_str = ", ".join(columns)
                values_insert_str = ", ".join("?" * column_count)
                update_clauses = ", ".join(
                    [f"{column} = excluded.{column}" for column in columns]
                )
                conn.executemany(
                    f"INSERT INTO {table} ({columns_insert_str}) VALUES ({values_insert_str}) ON CONFLICT DO UPDATE SET {update_clauses}",
                    data[table],
                )

    def init(self):
        with self.conn as conn:
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
                CREATE VIEW IF NOT EXISTS caculated AS
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
            ]

            for sql in create_sqls:
                conn.execute(sql)
            conn.commit()

    def __get_columns_from_dataclass(self, dataclass) -> List[str]:
        if is_dataclass(dataclass):
            dc_fields = fields(dataclass)
            return [field.name for field in dc_fields]
        return []

    def __get_columns_clause(self, columns: List[str]):
        return ", ".join([f'"{column}"' for column in columns])

    def get_packages(self):
        with self.conn as conn:
            columns_clause = self.__get_columns_clause(
                self.__get_columns_from_dataclass(DbPackageRow)
            )
            return [
                DbPackageRow(*row)
                for row in conn.execute(
                    f"SELECT {columns_clause} FROM packages"
                ).fetchall()
            ]

    def get_aliases(self):
        with self.conn as conn:
            columns_clause = self.__get_columns_clause(
                self.__get_columns_from_dataclass(DbAliasRow)
            )
            return [
                DbAliasRow(*row)
                for row in conn.execute(
                    f"SELECT {columns_clause} FROM aliases"
                ).fetchall()
            ]

    def get_aliases_by_song_id(self, song_id: str):
        with self.conn as conn:
            columns_clause = self.__get_columns_clause(
                self.__get_columns_from_dataclass(DbAliasRow)
            )
            return [
                DbAliasRow(*row)
                for row in (
                    conn.execute(
                        f"SELECT {columns_clause} FROM aliases WHERE song_id = ?",
                        (song_id,),
                    ).fetchall()
                )
            ]

    def get_charts(self):
        with self.conn as conn:
            columns_clause = self.__get_columns_clause(
                self.__get_columns_from_dataclass(DbChartRow)
            )
            return [
                DbChartRow(*row)
                for row in conn.execute(
                    f"SELECT {columns_clause} FROM charts"
                ).fetchall()
            ]

    def get_charts_by_song_id(self, song_id: str):
        with self.conn as conn:
            columns_clause = self.__get_columns_clause(
                self.__get_columns_from_dataclass(DbChartRow)
            )
            return [
                DbChartRow(*row)
                for row in (
                    conn.execute(
                        f"SELECT {columns_clause} FROM charts WHERE song_id = ?",
                        (song_id,),
                    ).fetchall()
                )
            ]

    def get_charts_by_package_id(self, package_id: str):
        with self.conn as conn:
            columns_clause = self.__get_columns_clause(
                self.__get_columns_from_dataclass(DbChartRow)
            )
            return [
                DbChartRow(*row)
                for row in conn.execute(
                    f"SELECT {columns_clause} FROM charts WHERE package_id = ?",
                    (package_id,),
                ).fetchall()
            ]

    def get_scores(
        self,
        *,
        song_id: Optional[List[str]] = None,
        rating_class: Optional[List[int]] = None,
    ):
        with self.conn as conn:
            columns = ",".join([f"[{field.name}]" for field in fields(DbScoreRow)])
            where_clauses = []
            params = []
            if song_id:
                where_clauses.append(f"song_id IN ({','.join('?'*len(song_id))})")
                params.extend(song_id)
            if rating_class:
                where_clauses.append(
                    f"rating_class IN ({','.join('?'*len(rating_class))})"
                )
                params.extend(rating_class)
            final_sql = f"SELECT {columns} FROM scores"
            if where_clauses:
                final_sql += " WHERE "
                final_sql += " AND ".join(where_clauses)
            return [
                DbScoreRow(*row) for row in conn.execute(final_sql, params).fetchall()
            ]

    def get_caculated(
        self,
        *,
        song_id: Optional[List[str]] = None,
        rating_class: Optional[List[int]] = None,
    ):
        with self.conn as conn:
            columns = ",".join([f"[{field.name}]" for field in fields(DbCaculatedRow)])
            where_clauses = []
            params = []
            if song_id:
                where_clauses.append(f"song_id IN ({','.join('?'*len(song_id))})")
                params.extend(song_id)
            if rating_class:
                where_clauses.append(
                    f"rating_class IN ({','.join('?'*len(rating_class))})"
                )
                params.extend(rating_class)
            final_sql = f"SELECT {columns} FROM caculated"
            if where_clauses:
                final_sql += " WHERE "
                final_sql += " AND ".join(where_clauses)
            return [
                DbCaculatedRow(*row)
                for row in conn.execute(final_sql, params).fetchall()
            ]

    def get_b30(self) -> float:
        with self.conn as conn:
            return conn.execute(
                """
            WITH max_potential AS (
                SELECT
                    song_id,
                    rating_class,
                    MAX(potential) AS max_potential
                FROM
                    caculated
                GROUP BY
                    song_id,
                    rating_class
            )
            SELECT
                SUM(potential) / (COUNT(potential) * 1.0) AS b30
            FROM
                (
                    SELECT
                        c.*
                    FROM
                        caculated c
                        JOIN max_potential m ON c.song_id = m.song_id AND c.rating_class = m.rating_class AND c.potential = m.max_potential
                    ORDER BY
                        potential DESC
                    LIMIT 30
                ) AS top_30

            """
            ).fetchone()[0]

    def insert_score(self, score: DbScoreRow):
        columns = self.__get_columns_from_dataclass(DbScoreRow)
        columns_clause = self.__get_columns_clause(columns)
        params = [score.__getattribute__(column) for column in columns]
        with self.conn as conn:
            conn.execute(
                f"INSERT INTO scores({columns_clause}) VALUES ({', '.join('?' * len(params))})",
                params,
            )
            conn.commit()
