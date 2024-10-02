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
            export_item: ArcaeaOfflineDEFv2PlayResultItem = {
                "id": item.id,
                "songId": item.song_id,
                "ratingClass": item.rating_class.value,
                "score": item.score,
                "pure": item.pure,
                "far": item.far,
                "lost": item.lost,
                "date": int(item.date.timestamp() * 1000) if item.date else 0,
                "maxRecall": item.max_recall,
                "modifier": (
                    item.modifier.value if item.modifier is not None else None
                ),
                "clearType": (
                    item.clear_type.value if item.clear_type is not None else None
                ),
                "source": "https://arcaeaoffline.sevive.xyz/python",
                "comment": item.comment,
            }

            export_items.append(export_item)

        return {
            "$schema": "https://arcaeaoffline.sevive.xyz/schemas/def/v2/score.schema.json",
            "type": "score",
            "version": 2,
            "scores": export_items,
        }
