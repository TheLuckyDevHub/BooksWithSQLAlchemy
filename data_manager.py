from data_models import Book, Author
from sqlalchemy.exc import IntegrityError

class DataManager:
    """
    Manages the data for the book and author database.
    """
    def __init__(self, db):
        self.db = db

    def add_Author(self,
                   name: str,
                   birth_date: str,
                   date_of_death: str) -> Author:
        """
        Adds a new author to the database.

        Args:
            name (str): The name of the author.
            birth_date (str): The birth date of the author.
            date_of_death (str): The date of death of the author.

        Returns:
            Author: The newly created Author object.
        """
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death)

        try:
            self.db.session.add(new_author)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise
        
        return new_author

    def exist_author(
        self,
        name: str,
        birth_date: str,
        date_of_death: str) -> bool:
        """
        Checks if an author with the given details exists in the database.

        Args:
            name (str): The name of the author.
            birth_date (str): The birth date of the author.
            date_of_death (str): The date of death of the author.

        Returns:
            bool: True if the author exists, False otherwise.
        """
        return self.db.session.query(
            Author).filter(
                Author.name == name,
                Author.birth_date == birth_date,
                Author.date_of_death == date_of_death).first() is not None

    def exist_book_isbn(self, isbn: str) -> bool:
        """
        Checks if a book with the given ISBN exists in the database.

        Args:
            isbn (str): The ISBN of the book.

        Returns:
            bool: True if the book exists, False otherwise.
        """
        return self.db.session.query(
            Book).filter(
                Book.isbn == isbn).first() is not None

    def exist_book_by_autor_and_title(self, author_id: int, title: str) -> bool:
        """
        Checks if a book with the given author ID and title exists in the database.

        Args:
            author_id (int): The ID of the author of the book.
            title (str): The title of the book.
        """
        return self.db.session.query(
            Book).filter(
                Book.author_id == author_id,
                Book.title == title).first() is not None

    def add_Book(self,
                 isbn: str,
                 title: str,
                 publication_year: int,
                 author_id: int) -> Book:
        """
        Adds a new book to the database.

        Args:
            isbn (str): The ISBN of the book.
            title (str): The title of the book.
            publication_year (int): The publication year of the book.
            author_id (int): The ID of the author of the book.

        Returns:
            Book: The newly created Book object.
        """
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=int(publication_year),
            author_id=int(author_id),
        )
        try:
            self.db.session.add(new_book)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

        return new_book
  
    def get_all_authors(self) -> list[Author]:
        """
        Retrieves all authors from the database, ordered by name.

        Returns:
            list[Author]: A list of all Author objects.
        """
       
        return self.db.session.query(Author).order_by(Author.name).all()
    
    def get_all_books(self) -> list[Book]:
        """
        Retrieves all books from the database, ordered by author ID and title.

        Returns:
            list[Book]: A list of all Book objects.
        """
        return self.db.session.query(Book).order_by(Book.author_id, Book.title).all()

    def get_all_books_with_authors(self) -> list[(Book, Author)]:
        """
        Retrieves all books with their authors, ordered by author name
        and book title.

        Returns:
            list[(Book, Author)]: A list of tuples, each containing a
            Book and its Author.
        """
        return (
            self.db.session.query(Book, Author)
            .order_by(Author.name, Book.title)
            .join(Author, Book.author_id == Author.id)
            .all()
        )

    def get_all_books_with_authors_order_by_(self, order_column: str):
        """
        Retrieves all books with their authors, ordered by a specified column.

        Args:
            order_column (str): The column to order the results by.

        Returns:
            list[(Book, Author)]: A list of tuples, each
            containing a Book and its Author.
        """
        return (
            self.db.session.query(Book, Author)
            .order_by(order_column)
            .join(Author, Book.author_id == Author.id)
            .all()
        )

    def get_all_books_with_authors_order_by_title(self) -> list[(Book, Author)]:
        """
        Retrieves all books with their authors, ordered by book title.

        Returns:
            list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
        """
        return self.get_all_books_with_authors_order_by_(Book.title)

    def get_all_books_with_authors_order_by_authors(self) -> list[(Book, Author)]:
        """
        Retrieves all books with their authors, ordered by author name.

        Returns:
            list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
        """
        return self.get_all_books_with_authors_order_by_(Author.name)

    def get_all_books_with_authors_order_by_publication_year(self) -> list[(Book, Author)]:
        """
        Retrieves all books with their authors, ordered by publication year.

        Returns:
            list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
        """
        return self.get_all_books_with_authors_order_by_(Book.publication_year)

    def get_all_books_with_authors_by_title(self, title: str) -> list[(Book, Author)]:
        """
        Searches for books by title and retrieves them with their authors.

        Args:
            title (str): The title to search for.

        Returns:
            list[(Book, Author)]: A list of tuples, each containing a matching Book and its Author.
        """
        return (
            self.db.session.query(Book, Author)
            .filter(Book.title.contains(title))
            .order_by(Book.title)
            .join(Author, Book.author_id == Author.id)
            .all()
        )
        
    def __delete_author_by_id(self, author_id: int):
        """
        Deletes an author by their ID.

        Args:
            author_id (int): The ID of the author to delete.
        """
        author = self.db.session.query(Author)\
            .filter(Author.id == author_id).first()
        if not author :
            return None
        try:
            self.db.session.delete(author)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
        return author
        
    def delete_book_by_id(self, book_id: int):
        """
        Deletes a book by its ID. If the author has no
        other books, the author is also deleted.

        Args:
            book_id (int): The ID of the book to delete.
        """
        book = self.db.session.query(Book).filter(Book.id == book_id).first()
        if book is None:
            return
        try:
            self.db.session.delete(book)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()

        books_by_author = (
            self.db.session.query(Book).filter(Book.author_id == book.author_id).count()
        )

        if books_by_author < 1:
            self.__delete_author_by_id(book.author_id)

    def get_author_by_id(self, author_id: int) -> Author:
        """
        Retrieves an author by their ID.
        """
        return self.db.session.query(Author)\
            .filter(Author.id == author_id).first()
