"""create books, authors, and book_authors tables

Revision ID: 8b57497ec434
Revises: 
Create Date: 2026-03-05 11:25:34.309680

"""
from sqlalchemy.sql import null
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b57497ec434'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, sa.Identity(always=True), primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('series', sa.String(50), nullable=True),
        sa.Column('genre', sa.String(50), nullable=True),
        sa.Column('first_pub', sa.Date, nullable=False),
        sa.Column('ver_edition', sa.Date, nullable=False),
        sa.Column('author_first', sa.String(50), nullable=False),
        sa.Column('author_last', sa.String(50), nullable=False),
        sa.Column('pub_name', sa.String(100), nullable=False),
        sa.Column('date_added', sa.Date, nullable=False)
    )

    op.create_table(
        'authors',
        sa.Column('id', sa.Integer, sa.Identity(always=True), primary_key=True),
        sa.Column('author_first', sa.String(length=50), nullable=False),
        sa.Column('author_last', sa.String(length=50), nullable=False)
    )
    #unique constraint to keep from multiple authors of the same name added
    #may need revision if exact name is truly different and added to the DB
    op.create_unique_constraint(
        constraint_name='unique author',
        table_name='authors',
        columns=['author_first', 'author_last']
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('books')
