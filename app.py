import os
from flask import Flask, render_template, request, redirect
from data_models import db, Author, Book

# basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(os.path.dirname(__file__), "data/library.sqlite")
DATE_FORMAT = "%Y-%m-%d"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
db.init_app(app)

"""Need only run once for create the database tables """
"""
with app.app_context():
  db.create_all()
"""


def get_all_authors() -> list[Author]:
    """
    Retrieves all authors from the database, ordered by name.

    Returns:
        list[Author]: A list of all Author objects.
    """
    return db.session.query(Author).order_by(Author.name).all()


def get_author_by_id(authors: list[Author], author_id: int) -> Author:
    """
    Finds an author by their ID from a list of authors.

    Args:
        authors (list[Author]): The list of authors to search.
        author_id (int): The ID of the author to find.

    Returns:
        Author: The Author object with the matching ID.
    """
    return [a for a in authors if a.id == author_id][0]


def get_all_books() -> list[Book]:
    """
    Retrieves all books from the database, ordered by author ID and title.

    Returns:
        list[Book]: A list of all Book objects.
    """
    return db.session.query(Book).order_by(Book.author_id, Book.title).all()


def get_all_books_with_authors() -> list[(Book, Author)]:
    """
    Retrieves all books with their authors, ordered by author name and book title.

    Returns:
        list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
    """
    return (
        db.session.query(Book, Author)
        .order_by(Author.name, Book.title)
        .join(Author, Book.author_id == Author.id)
        .all()
    )


def get_all_books_with_authors_order_by_(order_column: str):
    """
    Retrieves all books with their authors, ordered by a specified column.

    Args:
        order_column (str): The column to order the results by.

    Returns:
        list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
    """
    return (
        db.session.query(Book, Author)
        .order_by(order_column)
        .join(Author, Book.author_id == Author.id)
        .all()
    )


def get_all_books_with_authors_order_by_title() -> list[(Book, Author)]:
    """
    Retrieves all books with their authors, ordered by book title.

    Returns:
        list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
    """
    return get_all_books_with_authors_order_by_(Book.title)


def get_all_books_with_authors_order_by_authors() -> list[(Book, Author)]:
    """
    Retrieves all books with their authors, ordered by author name.

    Returns:
        list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
    """
    return get_all_books_with_authors_order_by_(Author.name)


def get_all_books_with_authors_order_by_publication_year() -> list[(Book, Author)]:
    """
    Retrieves all books with their authors, ordered by publication year.

    Returns:
        list[(Book, Author)]: A list of tuples, each containing a Book and its Author.
    """
    return get_all_books_with_authors_order_by_(Book.publication_year)


def get_all_books_with_authors_by_title(title: str) -> list[(Book, Author)]:
    """
    Searches for books by title and retrieves them with their authors.

    Args:
        title (str): The title to search for.

    Returns:
        list[(Book, Author)]: A list of tuples, each containing a matching Book and its Author.
    """
    return (
        db.session.query(Book, Author)
        .filter(Book.title.contains(title))
        .order_by(Book.title)
        .join(Author, Book.author_id == Author.id)
        .all()
    )


def delete_book_by_id(book_id):
    """
    Deletes a book by its ID. If the author has no other books, the author is also deleted.

    Args:
        book_id (int): The ID of the book to delete.
    """
    book = db.session.query(Book).filter(Book.id == book_id).first()
    db.session.delete(book)
    db.session.commit()
    books_by_author = (
        db.session.query(Book).filter(Book.author_id == book.author_id).count()
    )

    if books_by_author < 1:
        author = db.session.query(Author).filter(Author.id == book.author_id).first()
        db.session.delete(author)
        db.session.commit()


@app.route("/", methods=["GET"])
def home():
    """
    Renders the home page, displaying a list of books that can be sorted.
    """
    books_with_authors = []
    if "sort_by" in request.args.keys():
        sort_by = request.args["sort_by"]
        if sort_by == "title":
            books_with_authors = get_all_books_with_authors_order_by_title()
        elif sort_by == "author":
            books_with_authors = get_all_books_with_authors_order_by_authors()
        elif sort_by == "year":
            books_with_authors = get_all_books_with_authors_order_by_publication_year()
        else:
            books_with_authors = get_all_books_with_authors()
    else:
        books_with_authors = get_all_books_with_authors()

    return render_template("home.html", books_with_authors=books_with_authors)


@app.route("/", methods=["POST"])
def home_post():
    """
    Handles the search form on the home page, filtering books by title.
    """
    title = request.form["title"]
    return render_template(
        "home.html", books_with_authors=get_all_books_with_authors_by_title(title)
    )


@app.route("/delete/<int:book_id>", methods=["GET", "POST"])
def delete(book_id):
    """
    Deletes a book and redirects to the home page.
    """
    delete_book_by_id(book_id)
    return redirect("/")


@app.route("/add_author", methods=["GET"])
def add_author():
    """
    Renders the page for adding a new author.
    """
    return render_template(
        "add_author.html",
        visibility_author_message="visibility:hidden",
        added_author_message="",
    )


@app.route("/add_author", methods=["POST"])
def add_author_post():
    """
    Handles the form for adding a new author.
    """
    name = request.form["name"]
    birth_date = request.form["birthdate"]
    date_of_death = request.form["date_of_death"]

    new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

    db.session.add(new_author)
    db.session.commit()

    message = f"The author {name} has been added successfully!"
    return (
        render_template(
            "add_author.html",
            visibility_author_message="",
            added_author_message=message,
        ),
        200,
    )


@app.route("/add_book", methods=["GET"])
def add_book():
    """
    Renders the page for adding a new book.
    """
    return render_template(
        "add_book.html",
        authors=get_all_authors(),
        visibility_book_message="",
        added_book_message="",
    )


@app.route("/add_book", methods=["POST"])
def add_book_post():
    """
    Handles the form for adding a new book.
    """
    isbn = request.form["isbn"]
    title = request.form["title"]
    publication_year = request.form["publication_year"]
    author_id = request.form["author_id"]

    new_book = Book(
        isbn=isbn,
        title=title,
        publication_year=int(publication_year),
        author_id=int(author_id),
    )

    print(new_book)
    db.session.add(new_book)
    db.session.commit()

    authors = get_all_authors()
    author: Author = get_author_by_id(authors, new_book.author_id)

    message = f"The book {title} form {author.name} has been added successfully!"
    return (
        render_template(
            "add_book.html",
            authors=authors,
            visibility_book_message="",
            added_book_message=message,
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
