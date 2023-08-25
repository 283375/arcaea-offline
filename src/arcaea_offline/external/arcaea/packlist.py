import json
from typing import List, Union

from ...models.songs import Pack, PackLocalized
from .common import ArcaeaParser, is_localized, set_model_localized_attrs


class PacklistParser(ArcaeaParser):
    def __init__(self, filepath):
        super().__init__(filepath)

    def parse(self) -> List[Union[Pack, PackLocalized]]:
        with open(self.filepath, "r", encoding="utf-8") as pl_f:
            packlist_json_root = json.loads(pl_f.read())

        packlist_json = packlist_json_root["packs"]
        results = []
        for item in packlist_json:
            pack = Pack()
            pack.id = item["id"]
            pack.name = item["name_localized"]["en"]
            pack.description = item["description_localized"]["en"] or None
            results.append(pack)

            if is_localized(item, "name") or is_localized(item, "description"):
                pack_localized = PackLocalized(id=pack.id)
                set_model_localized_attrs(pack_localized, item, "name")
                set_model_localized_attrs(pack_localized, item, "description")
                results.append(pack_localized)

        return results