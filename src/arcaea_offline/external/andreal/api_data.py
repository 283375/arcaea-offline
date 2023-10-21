from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models import CalculatedPotential, ScoreBest, ScoreCalculated
from .account import AndrealImageGeneratorAccount


class AndrealImageGeneratorApiDataConverter:
    def __init__(
        self,
        session: Session,
        account: AndrealImageGeneratorAccount = AndrealImageGeneratorAccount(),
    ):
        self.session = session
        self.account = account

    def account_info(self):
        return {
            "code": self.account.code,
            "name": self.account.name,
            "is_char_uncapped": self.account.character_uncapped,
            "rating": self.account.rating,
            "character": self.account.character,
        }

    def score(self, score: Union[ScoreCalculated, ScoreBest]):
        return {
            "score": score.score,
            "health": 75,
            "rating": score.potential,
            "song_id": score.song_id,
            "modifier": score.modifier or 0,
            "difficulty": score.rating_class,
            "clear_type": score.clear_type or 1,
            "best_clear_type": score.clear_type or 1,
            "time_played": score.date * 1000 if score.date else 0,
            "near_count": score.far,
            "miss_count": score.lost,
            "perfect_count": score.pure,
            "shiny_perfect_count": score.shiny_pure,
        }

    def user_info(self, score: Optional[ScoreCalculated] = None):
        if not score:
            score = self.session.scalar(
                select(ScoreCalculated).order_by(ScoreCalculated.date.desc()).limit(1)
            )
        if not score:
            raise ValueError("No score available.")

        return {
            "content": {
                "account_info": self.account_info(),
                "recent_score": [self.score(score)],
            }
        }

    def user_best(self, song_id: str, rating_class: int):
        score = self.session.scalar(
            select(ScoreBest).where(
                (ScoreBest.song_id == song_id)
                & (ScoreBest.rating_class == rating_class)
            )
        )
        if not score:
            raise ValueError("No score available.")

        return {
            "content": {
                "account_info": self.account_info(),
                "record": self.score(score),
            }
        }

    def user_best30(self):
        scores = list(
            self.session.scalars(
                select(ScoreBest).order_by(ScoreBest.potential.desc()).limit(40)
            )
        )
        if not scores:
            raise ValueError("No score available.")
        best30_avg = self.session.scalar(select(CalculatedPotential.b30))

        best30_overflow = (
            [self.score(score) for score in scores[30:40]] if len(scores) > 30 else []
        )

        return {
            "content": {
                "account_info": self.account_info(),
                "best30_avg": best30_avg,
                "best30_list": [self.score(score) for score in scores[:30]],
                "best30_overflow": best30_overflow,
            }
        }
