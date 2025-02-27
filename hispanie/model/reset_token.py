from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .resource import Resource

if TYPE_CHECKING:
    from .account import Account


class ResetToken(Base, Resource):
    __tablename__ = "reset_token"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # token

    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # foreign key
    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"))

    # relationship

    # Zero-to-Many relationship with account
    account: Mapped["Account"] = relationship("Account", back_populates="reset_tokens")
