from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from arcaea_offline.utils import Version

from ._base import ModelBase, ReprHelper


class VersionDate(ModelBase, ReprHelper):
    __tablename__ = "version_date"

    version: Mapped[Version] = mapped_column(primary_key=True)
    songlist_at: Mapped[datetime]
    published_at: Mapped[datetime]
