# Solution Steps

1. Normalize the database schema by creating separate 'authors' and 'categories' tables, and referencing them via foreign keys in the 'books' table.

2. Add unique constraints on author and category names, and relevant indexes on 'books.author_id', 'books.category_id', and 'books.title' columns, in the migration script. Set up ON DELETE CASCADE for referential integrity.

3. Update the ORM models to reflect relationships: Book has author_id/category_id, Author has books, Category has books.

4. Configure the async-aware SQLAlchemy database setup ('db.py') using create_async_engine and AsyncSession. Set up get_async_session for dependency injection.

5. Rewrite CRUD functions to use async session, optimized async queries, and joins—ensuring all operations (add, search, etc.) are non-blocking and leverage indexes.

6. When adding a book, upsert author/category records to avoid duplicates, using flush to get the new id if just created.

7. For search (by author/category), use joins on indexed columns and 'order_by' for deterministic query plans and fast results.

8. Ensure all operations in the CRUD file are wrapped in 'async with AsyncSessionLocal()' context and use 'await' on DB actions.

9. Apply the migration so the database schema includes all indexes and constraints. Now, the searches are fast, fully async, and schema is normalized.

