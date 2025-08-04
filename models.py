from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    books = relationship('Book', back_populates='category', cascade='all, delete-orphan')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False, index=True)
    publication_date = Column(Date, nullable=False)
    author = relationship('Author', back_populates='books')
    category = relationship('Category', back_populates='books')
