"""change column name for publisher

Revision ID: 10917e5ea5a6
Revises: 97b3a6c30907
Create Date: 2026-03-13 15:52:29.591854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10917e5ea5a6'
down_revision: Union[str, Sequence[str], None] = '97b3a6c30907'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('books', 'pub_name', new_column_name='publisher')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('books', 'publisher', new_column_name='pub_name')
