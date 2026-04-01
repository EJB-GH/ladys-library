"""change column name for version of book

Revision ID: 97b3a6c30907
Revises: 354339a97ab9
Create Date: 2026-03-13 15:44:31.539537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97b3a6c30907'
down_revision: Union[str, Sequence[str], None] = '354339a97ab9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('books', 'ver_edition', new_column_name='version') 


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('books', 'version', new_column_name='ver_edition')
