"""create book_authors table for real

Revision ID: b77ab9560b66
Revises: 8b57497ec434
Create Date: 2026-03-05 15:15:29.252039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b77ab9560b66'
down_revision: Union[str, Sequence[str], None] = '8b57497ec434'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'book_authors',
        sa.Column('book_id', sa.Integer, sa.ForeignKey('books.id'), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('authors.id'), nullable=False),
        sa.PrimaryKeyConstraint('book_id', 'author_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('book_authors')
