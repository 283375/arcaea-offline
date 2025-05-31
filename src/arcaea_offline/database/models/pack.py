from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import ModelBase, ReprHelper

if TYPE_CHECKING:
    from .song import Song


class Pack(ModelBase, ReprHelper):
    __tablename__ = "pack"

    songs: Mapped[list["Song"]] = relationship(
        back_populates="pack",
        cascade="all, delete",
        passive_deletes=True,
    )
    localized_entries: Mapped[list["PackLocalization"]] = relationship(
        back_populates="pack",
        cascade="all, delete",
        passive_deletes=True,
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    section: Mapped[Optional[str]] = mapped_column(String)
    is_world_extend: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )

    plus_character: Mapped[Optional[int]] = mapped_column(Integer)

    append_parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("pack.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    parent: Mapped["Pack"] = relationship(
        "Pack",
        back_populates="appendages",
        cascade="all, delete",
        passive_deletes=True,
        remote_side=[id],
    )
    appendages: Mapped[list["Pack"]] = relationship("Pack", back_populates="parent")


class PackLocalization(ModelBase, ReprHelper):
    __tablename__ = "pack_localization"

    pack: Mapped["Pack"] = relationship(back_populates="localized_entries")
    id: Mapped[str] = mapped_column(
        ForeignKey("pack.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    lang: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
