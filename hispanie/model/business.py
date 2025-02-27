from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..errors import NoBusinessFound
from ..utils import idv2
from .base import Base
from .entity import Entity

if TYPE_CHECKING:
    from .account import Account
    from .file import File
    from .social_network import SocialNetwork
    from .tag import Tag


class BusinessCategory(Enum):
    ARTIST = "artist"
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    BOUTIQUE = "boutique"
    EXPOSITION = "exposition"
    ASSOCIATION = "association"
    ACADEMY = "academy"


class Business(Base, Entity):
    __tablename__ = "business"
    __errors__ = {"_error": NoBusinessFound}

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("business", version=1)
    )

    category: Mapped[BusinessCategory] = mapped_column(SQLAEnum(BusinessCategory), nullable=False)

    # DONE add change name attr to title ? No
    # DONE add tags, another table or a list of strings ? yes table
    # DONE add artists, is it an accounts list with type artists ? no, it's a business
    # DONE add location: str ? latitude, longitude and city can be taken from location ?
    # DONE Add url or urls ? in Entity class ? yes and yes

    # foreign key

    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"), nullable=False)

    # relationships

    # One-to-Many relationship with account
    account: Mapped["Account"] = relationship("Account", back_populates="businesses")

    social_networks: Mapped[list["SocialNetwork"]] = relationship(
        "SocialNetwork", back_populates="business"
    )

    # Many-to-Many relationship with File
    files: Mapped[list["File"]] = relationship(
        "File",
        secondary="business_file",
        back_populates="businesses",
    )

    # Many-to-Many relationship with Tag
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="business_tag",
        back_populates="businesses",
    )
