"""add date_added to books for easy add history

Revision ID: a9a9953fcb93
Revises: b77ab9560b66
Create Date: 2026-03-05 16:34:53.038099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a9953fcb93'
down_revision: Union[str, Sequence[str], None] = 'b77ab9560b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('books', sa.Column('date_added', sa.Date, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('books', 'date_added')
