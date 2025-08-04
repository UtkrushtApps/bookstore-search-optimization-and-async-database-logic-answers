from sqlalchemy.future import select
from sqlalchemy import insert, func
from sqlalchemy.exc import NoResultFound
from models import Book, Author, Category
from db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

# Create (add) a book with upsert for author/category
async def add_book(book_in):
    async with AsyncSessionLocal() as session:
        # Get or create author
        result = await session.execute(select(Author).where(Author.name == book_in.author))
        author = result.scalars().first()
        if not author:
            author = Author(name=book_in.author)
            session.add(author)
            await session.flush()  # to get id
        # Get or create category
        result = await session.execute(select(Category).where(Category.name == book_in.category))
        category = result.scalars().first()
        if not category:
            category = Category(name=book_in.category)
            session.add(category)
            await session.flush()
        # Create the book
        book = Book(
            title=book_in.title,
            author_id=author.id,
            category_id=category.id,
            publication_date=book_in.publication_date
        )
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

# Async query to get books by author (optimized index lookup/join)
async def get_books_by_author(author_name: str):
    async with AsyncSessionLocal() as session:
        query = (
            select(Book)
            .join(Author)
            .where(Author.name == author_name)
            .order_by(Book.publication_date.desc())
        )
        result = await session.execute(query)
        books = result.scalars().all()
        return books

# Async query to get books by category (optimized index lookup/join)
async def get_books_by_category(category_name: str):
    async with AsyncSessionLocal() as session:
        query = (
            select(Book)
            .join(Category)
            .where(Category.name == category_name)
            .order_by(Book.publication_date.desc())
        )
        result = await session.execute(query)
        books = result.scalars().all()
        return books
