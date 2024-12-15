from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .resource import Resource


# Association Class for Many-to-Many relationship
class BusinessFile(Base, Resource):
    __tablename__ = "business_file"

    business_id: Mapped[str] = mapped_column(ForeignKey("business.id"), primary_key=True)

    file_id: Mapped[str] = mapped_column(ForeignKey("file.id"), primary_key=True)
