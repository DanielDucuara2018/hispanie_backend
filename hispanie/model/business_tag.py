from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from hispanie.model.base import Base
from hispanie.model.resource import Resource


# Association Class for Many-to-Many relationship
class BusinessTag(Base, Resource):
    __tablename__ = "business_tag"

    business_id: Mapped[str] = mapped_column(ForeignKey("business.id"), primary_key=True)

    tag_id: Mapped[str] = mapped_column(ForeignKey("tag.id"), primary_key=True)
