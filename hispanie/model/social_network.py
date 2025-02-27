from enum import Enum

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base
from .business import Business
from .resource import Resource


class SocialNetworkCategory(Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    WEB = "web"


class SocialNetwork(Base, Resource):
    __tablename__ = "social_network"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("social_network", version=1)
    )

    url: Mapped[str] = mapped_column(String, nullable=False)

    category: Mapped[SocialNetworkCategory] = mapped_column(
        SQLAEnum(SocialNetworkCategory), nullable=False
    )

    # foreign key
    business_id: Mapped[str] = mapped_column(ForeignKey("business.id"))

    # relationship

    # Zero-to-Many relationship with Business
    business: Mapped["Business"] = relationship("Business", back_populates="social_networks")
