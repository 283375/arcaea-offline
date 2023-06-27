import atexit
import os
import sqlite3
from dataclasses import fields, is_dataclass
from typing import Callable, List, NamedTuple, Optional, TypeVar, Union

from thefuzz import fuzz
from thefuzz import process as fuzz_process

from .init_sqls import INIT_SQLS
from .models import (
    DbAliasRow,
    DbCalculatedRow,
    DbChartRow,
    DbPackageRow,
    DbScoreRow,
    ScoreInsert,
)
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

        atexit.register(self.__conn.close)

        self.__update_hooks = []

    @property
    def conn(self):
        return self.__conn

    def register_update_hook(self, hook: Callable) -> bool:
        if callable(hook):
            if hook not in self.__update_hooks:
                self.__update_hooks.append(hook)
            return True
        return False

    def unregister_update_hook(self, hook: Callable) -> bool:
        if hook in self.__update_hooks:
            self.__update_hooks.remove(hook)
            return True
        return False

    def __trigger_update_hooks(self):
        for hook in self.__update_hooks:
            hook()

    def update_arcsong_db(self, path: Union[str, bytes]):
        with sqlite3.connect(path) as arcsong_conn:
            arcsong_cursor = arcsong_conn.cursor()
            data = {
                "charts": arcsong_cursor.execute(
                    "SELECT song_id, rating_class, name_en, name_jp, artist, bpm, bpm_base, [set], time, side, world_unlock, remote_download, bg, date, version, difficulty, rating, note, chart_designer, jacket_designer, jacket_override, audio_override FROM charts"
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
        create_sqls = INIT_SQLS[1]["init"]

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

    def get_package_by_package_id(self, package_id: str):
        result = self.__get_table(
            "packages", DbPackageRow, "package_id = ?", (package_id,)
        )
        return result[0] if result else None

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

    def get_chart(self, song_id: str, rating_class: int):
        return self.__get_table(
            "charts",
            DbChartRow,
            "song_id = ? AND rating_class = ?",
            (song_id, rating_class),
        )[0]

    def validate_song_id(self, song_id):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM charts WHERE song_id = ?", (song_id,))
            result = cursor.fetchone()
            return result[0] > 0

    def validate_chart(self, song_id: str, rating_class: int):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM charts WHERE song_id = ? AND rating_class = ?",
                (song_id, rating_class),
            )
            result = cursor.fetchone()
            return result[0] > 0

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

    def insert_score(self, score: ScoreInsert):
        columns = self.__get_columns_from_dataclass(ScoreInsert)
        columns_clause = self.__get_columns_clause(columns)
        params = [getattr(score, column) for column in columns]
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO scores({columns_clause}) VALUES ({', '.join('?' * len(params))})",
                params,
            )
            conn.commit()
            self.__trigger_update_hooks()

    def delete_score(self, score_id: int):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM scores WHERE id = ?", (score_id,))
            conn.commit()
            self.__trigger_update_hooks()
