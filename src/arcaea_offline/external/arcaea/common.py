import contextlib
import json
import math
import time
from os import PathLike
from typing import Any, List, Optional, Union

from sqlalchemy.orm import DeclarativeBase, Session


def fix_timestamp(timestamp: int) -> Union[int, None]:
    """
    Some of the `date` column in st3 are strangely truncated. For example,
    a `1670283375` may be truncated to `167028`, even `1`. Yes, a single `1`.

    To properly handle this situation, we check the timestamp's digits.
    If `digits < 5`, we treat this timestamp as a `None`. Otherwise, we try to
    fix the timestamp.

    :param timestamp: a POSIX timestamp
    :return: `None` if the timestamp's digits < 5, otherwise a fixed POSIX timestamp
    """
    # find digit length from https://stackoverflow.com/a/2189827/16484891
    # CC BY-SA 2.5
    # this might give incorrect result when timestamp > 999999999999997,
    # see https://stackoverflow.com/a/28883802/16484891 (CC BY-SA 4.0).
    # but that's way too later than 9999-12-31 23:59:59, 253402271999,
    # I don't think Arcaea would still be an active updated game by then.
    # so don't mind those small issues, just use this.
    digits = int(math.log10(abs(timestamp))) + 1 if timestamp != 0 else 1
    if digits < 5:
        return None
    timestamp_str = str(timestamp)
    current_timestamp_digits = int(math.log10(int(time.time()))) + 1
    timestamp_str = timestamp_str.ljust(current_timestamp_digits, "0")
    return int(timestamp_str, 10)


def to_db_value(val: Any) -> Any:
    if not val:
        return None
    return json.dumps(val, ensure_ascii=False) if isinstance(val, list) else val


def is_localized(item: dict, key: str, append_localized: bool = True):
    item_key = f"{key}_localized" if append_localized else key
    subitem: Optional[dict] = item.get(item_key)
    return subitem and (
        subitem.get("ja")
        or subitem.get("ko")
        or subitem.get("zh-Hant")
        or subitem.get("zh-Hans")
    )


def set_model_localized_attrs(
    model: DeclarativeBase, item: dict, model_key: str, item_key: Optional[str] = None
):
    if item_key is None:
        item_key = f"{model_key}_localized"
    subitem: dict = item.get(item_key, {})
    if not subitem:
        return
    setattr(model, f"{model_key}_ja", to_db_value(subitem.get("ja")))
    setattr(model, f"{model_key}_ko", to_db_value(subitem.get("ko")))
    setattr(model, f"{model_key}_zh_hans", to_db_value(subitem.get("zh-Hans")))
    setattr(model, f"{model_key}_zh_hant", to_db_value(subitem.get("zh-Hant")))


class ArcaeaParser:
    def __init__(self, filepath: Union[str, bytes, PathLike]):
        self.filepath = filepath

    def read_file_text(self):
        file_handle = None

        with contextlib.suppress(TypeError):
            # original open
            file_handle = open(self.filepath, "r", encoding="utf-8")

        if file_handle is None:
            try:
                # or maybe a `pathlib.Path` subset
                # or an `importlib.resources.abc.Traversable` like object
                # e.g. `zipfile.Path`
                file_handle = self.filepath.open(mode="r", encoding="utf-8")  # type: ignore
            except Exception as e:
                raise ValueError("Invalid `filepath`.") from e

        with file_handle:
            return file_handle.read()

    def parse(self) -> List[DeclarativeBase]:
        raise NotImplementedError()

    def write_database(self, session: Session):
        results = self.parse()
        for result in results:
            session.merge(result)
