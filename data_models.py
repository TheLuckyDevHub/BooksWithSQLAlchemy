from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author of a book.

    Attributes:
        id (int): The unique identifier for the author.
        name (str): The name of the author.
        birth_date (str): The birth date of the author.
        date_of_death (str, optional): The date of death of the author. Defaults to None.
    """

    __tablename__ = "authors"

    id: int = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String, nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Author object.
        """
        if self.date_of_death is None:
            return f"<{type(self).__name__}><id {self.id}><Author {self.name}><Birth date {self.birth_date}><Death Date {self.date_of_death}>"

        return f"<{type(self).__name__}><id {self.id}><Author {self.name}><Birth date {self.birth_date}>"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Author object.
        """
        if self.date_of_death is None:
            return f"{self.name}, {self.birth_date}"

        return f"{self.name}, {self.birth_date} - {self.date_of_death}"


class Book(db.Model):
    """
    Represents a book.

    Attributes:
        id (int): The unique identifier for the book.
        isbn (str): The ISBN of the book.
        title (str): The title of the book.
        publication_year (str): The publication year of the book.
        author_id (int): The foreign key of the author.
    """

    __tablename__ = "books"

    id: int = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the Book object.
        """
        return f"<{type(self).__name__}><id {self.id}> <Title {self.title}><ISBN {self.isbn}><Publication year {self.publication_year}><Author id {self.author_id}>"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Book object.
        """
        return f"{self.title} {self.isbn} {self.publication_year} {self.author_id}"
