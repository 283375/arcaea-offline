import statistics
from dataclasses import dataclass
from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models import (
    PlayResultBest,
    PlayResultCalculated,
)

from .definitions import (
    AndrealImageGeneratorApiDataAccountInfo,
    AndrealImageGeneratorApiDataRoot,
    AndrealImageGeneratorApiDataScoreItem,
)


@dataclass
class AndrealImageGeneratorAccount:
    name: str = "Player"
    code: int = 123456789
    rating: int = -1
    character: int = 5
    character_uncapped: bool = False


class AndrealImageGeneratorApiDataExporter:
    @staticmethod
    def craft_account_info(
        account: AndrealImageGeneratorAccount,
    ) -> AndrealImageGeneratorApiDataAccountInfo:
        return {
            "code": account.code,
            "name": account.name,
            "is_char_uncapped": account.character_uncapped,
            "rating": account.rating,
            "character": account.character,
        }

    @staticmethod
    def craft_score_item(
        play_result: Union[PlayResultCalculated, PlayResultBest],
    ) -> AndrealImageGeneratorApiDataScoreItem:
        modifier = play_result.modifier.value if play_result.modifier else 0
        clear_type = play_result.clear_type.value if play_result.clear_type else 0

        return {
            "score": play_result.score,
            "health": 75,
            "rating": play_result.potential,
            "song_id": play_result.song_id,
            "modifier": modifier,
            "difficulty": play_result.rating_class.value,
            "clear_type": clear_type,
            "best_clear_type": clear_type,
            "time_played": int(play_result.date.timestamp() * 1000)
            if play_result.date
            else 0,
            "near_count": play_result.far,
            "miss_count": play_result.lost,
            "perfect_count": play_result.pure,
            "shiny_perfect_count": play_result.shiny_pure,
        }

    @classmethod
    def user_info(
        cls,
        play_result_calculated: PlayResultCalculated,
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
    ) -> AndrealImageGeneratorApiDataRoot:
        return {
            "content": {
                "account_info": cls.craft_account_info(account),
                "recent_score": [cls.craft_score_item(play_result_calculated)],
            }
        }

    @classmethod
    def user_best(
        cls,
        play_result_best: PlayResultBest,
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
    ) -> AndrealImageGeneratorApiDataRoot:
        return {
            "content": {
                "account_info": cls.craft_account_info(account),
                "record": cls.craft_score_item(play_result_best),
            }
        }

    @classmethod
    def user_best30(
        cls,
        play_results_best: List[PlayResultBest],
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
    ) -> AndrealImageGeneratorApiDataRoot:
        play_results_best_sorted = sorted(
            play_results_best, key=lambda it: it.potential, reverse=True
        )

        best30_list = play_results_best_sorted[:30]
        best30_overflow = play_results_best_sorted[30:]

        best30_avg = statistics.fmean([it.potential for it in best30_list])

        return {
            "content": {
                "account_info": cls.craft_account_info(account),
                "best30_avg": best30_avg,
                "best30_list": [cls.craft_score_item(it) for it in best30_list],
                "best30_overflow": [cls.craft_score_item(it) for it in best30_overflow],
            }
        }

    @classmethod
    def craft_user_info(
        cls,
        session: Session,
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
    ) -> Optional[AndrealImageGeneratorApiDataRoot]:
        play_result_calculated = session.scalar(
            select(PlayResultCalculated)
            .order_by(PlayResultCalculated.date.desc())
            .limit(1)
        )

        if play_result_calculated is None:
            return None

        return cls.user_info(play_result_calculated, account)

    @classmethod
    def craft_user_best(
        cls,
        session: Session,
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
        *,
        song_id: str,
        rating_class: ArcaeaRatingClass,
    ):
        play_result_best = session.scalar(
            select(PlayResultBest).where(
                (PlayResultBest.song_id == song_id)
                & (PlayResultBest.rating_class == rating_class)
            )
        )

        if play_result_best is None:
            return None

        return cls.user_best(play_result_best, account)

    @classmethod
    def craft(
        cls,
        session: Session,
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
        *,
        limit: int = 40,
    ) -> Optional[AndrealImageGeneratorApiDataRoot]:
        play_results_best = list(
            session.scalars(
                select(PlayResultBest)
                .order_by(PlayResultBest.potential.desc())
                .limit(limit)
            ).all()
        )

        return cls.user_best30(play_results_best, account)
