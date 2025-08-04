"""
Revision for optimized Book schema with relevant indexes and foreign keys.
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create author and category tables for normalization
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False)
    )
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False)
    )
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('publication_date', sa.Date, nullable=False)
    )
    # Add indexes for search optimization
    op.create_index('ix_books_author_id', 'books', ['author_id'])
    op.create_index('ix_books_category_id', 'books', ['category_id'])
    op.create_index('ix_books_title', 'books', ['title'])

def downgrade():
    op.drop_index('ix_books_title', table_name='books')
    op.drop_index('ix_books_category_id', table_name='books')
    op.drop_index('ix_books_author_id', table_name='books')
    op.drop_table('books')
    op.drop_table('categories')
    op.drop_table('authors')
