"""rename user table and add unique email

Revision ID: 00900f89be09
Revises: 095a5e40830d
Create Date: 2026-10-25 19:49:15.886781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '00900f89be09'
down_revision: Union[str, Sequence[str], None] = '095a5e40830d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("user", "users")

    op.create_unique_constraint(
        "uq_users_email",
        "users",
        ["email"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique",
    )

    op.rename_table("users", "user")
