"""add product cost price

Revision ID: e8e0a1d4f2b7
Revises: 71e35b228ce5
Create Date: 2026-06-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e8e0a1d4f2b7"
down_revision: Union[str, Sequence[str], None] = "71e35b228ce5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "product",
        sa.Column("cost_price", sa.Numeric(10, 2), nullable=True, comment="进货价"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("product", "cost_price")
