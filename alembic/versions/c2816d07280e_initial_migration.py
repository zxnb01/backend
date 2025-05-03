"""Initial migration

Revision ID: c2816d07280e
Revises: c83ead7f1518
Create Date: 2025-05-03 16:53:18.275498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2816d07280e'
down_revision: Union[str, None] = 'c83ead7f1518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
