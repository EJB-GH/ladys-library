"""reduce redundancy in books table <removal of authors components>

Revision ID: 354339a97ab9
Revises: a9a9953fcb93
Create Date: 2026-03-10 09:18:31.682043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '354339a97ab9'
down_revision: Union[str, Sequence[str], None] = 'a9a9953fcb93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('books', 'author_first')
    op.drop_column('books', 'author_last')


def downgrade() -> None:
    """Downgrade schema."""
    pass
    
