"""0002 Added unique constraint account.

Revision ID: 4e5378918657
Revises: c5614ae0da1b
Create Date: 2025-03-25 20:48:37.184597

"""

from typing import Sequence

import sqlalchemy as sa  # noqa: F401

from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision: str = "4e5378918657"
down_revision: str | None = "c5614ae0da1b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("account_email_key", "account", type_="unique")
    op.create_unique_constraint(op.f("uq_account_email"), "account", ["email"])
    op.create_unique_constraint(op.f("uq_account_username"), "account", ["username"])
    op.drop_constraint("tag_name_key", "tag", type_="unique")
    op.create_unique_constraint(op.f("uq_tag_name"), "tag", ["name"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_tag_name"), "tag", type_="unique")
    op.create_unique_constraint("tag_name_key", "tag", ["name"])
    op.drop_constraint(op.f("uq_account_username"), "account", type_="unique")
    op.drop_constraint(op.f("uq_account_email"), "account", type_="unique")
    op.create_unique_constraint("account_email_key", "account", ["email"])
    # ### end Alembic commands ###
