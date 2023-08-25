import json
from os import PathLike
from typing import Any, List, Optional, Union

from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase, Session


def to_db_value(val: Any) -> Any:
    if not val:
        return None
    elif isinstance(val, list):
        return json.dumps(val, ensure_ascii=False)
    else:
        return val


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

    def parse(self) -> List[DeclarativeBase]:
        ...

    def write_database(self, engine: Engine):
        with Session(engine) as session:
            results = self.parse()
            for result in results:
                session.merge(result)
            session.commit()
