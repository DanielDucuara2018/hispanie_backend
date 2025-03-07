from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idun
from .base import Base
from .business import Business
from .event import Event
from .resource import Resource

if TYPE_CHECKING:
    from .account import Account


class FileCategory(Enum):
    PROFILE_IMAGE = "profile_image"
    COVER_IMAGE = "cover_image"


class File(Base, Resource):
    __tablename__ = "file"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: idun("file"))

    filename: Mapped[str] = mapped_column(String, nullable=False)

    content_type: Mapped[str] = mapped_column(String, nullable=False)

    category: Mapped[FileCategory] = mapped_column(SQLAEnum(FileCategory), nullable=False)

    path: Mapped[str] = mapped_column(String, nullable=False)

    hash: Mapped[str] = mapped_column(String, nullable=False)

    # foreign key
    account_id: Mapped[str | None] = mapped_column(ForeignKey("account.id"))

    event_id: Mapped[str | None] = mapped_column(ForeignKey("event.id"))

    business_id: Mapped[str | None] = mapped_column(ForeignKey("business.id"))

    # relationship

    # Zero-to-Many relationship with account
    account: Mapped["Account"] = relationship("Account", back_populates="files")

    event: Mapped["Event"] = relationship("Event", back_populates="files")

    business: Mapped["Business"] = relationship("Business", back_populates="files")
