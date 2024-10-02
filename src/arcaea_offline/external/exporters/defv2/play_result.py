from typing import List

from arcaea_offline.database.models import PlayResult

from .definitions import (
    ArcaeaOfflineDEFv2PlayResultItem,
    ArcaeaOfflineDEFv2PlayResultRoot,
)


class ArcaeaOfflineDEFv2PlayResultExporter:
    def export(self, items: List[PlayResult]) -> ArcaeaOfflineDEFv2PlayResultRoot:
        export_items = []
        for item in items:
            export_item: ArcaeaOfflineDEFv2PlayResultItem = {}

            export_item["id"] = item.id
            export_item["songId"] = item.song_id
            export_item["ratingClass"] = item.rating_class.value
            export_item["score"] = item.score
            export_item["pure"] = item.pure
            export_item["far"] = item.far
            export_item["lost"] = item.lost
            export_item["date"] = item.date
            export_item["maxRecall"] = item.max_recall
            export_item["modifier"] = (
                item.modifier.value if item.modifier is not None else None
            )
            export_item["clearType"] = (
                item.clear_type.value if item.clear_type is not None else None
            )
            export_item["source"] = "https://arcaeaoffline.sevive.xyz/python"
            export_item["comment"] = item.comment

        return {
            "$schema": "https://arcaeaoffline.sevive.xyz/schemas/def/v2/score.schema.json",
            "type": "score",
            "version": 2,
            "scores": export_items,
        }
