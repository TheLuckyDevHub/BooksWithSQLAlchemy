import os
from flask import Flask, render_template, request, redirect
from data_models import db, Author
from data_manager import DataManager
from datetime import datetime
from isbnlib import is_isbn13, is_isbn10


# basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(os.path.dirname(__file__), "data/library.sqlite")
DATE_FORMAT = "%Y-%m-%d"
DATE_PRINT_FORMAT = "%m/%d/%Y"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
db.init_app(app)
data_manager = DataManager(db)

"""Need only run once for create the database tables """
"""
with app.app_context():
  db.create_all()
"""


# gets a datetime object from string format 2000-12-20
def get_date_from_str(str_date: str) -> datetime.date:
    result: datetime.date = None
    if str_date == "":
        return None
    try:
        result = datetime.strptime(str_date, DATE_FORMAT).date()  
    except ValueError:
        return None
    return result


def get_date_print_format(date: datetime.date) -> str:
    return date.strftime(DATE_PRINT_FORMAT)


@app.route("/", methods=["GET"])
def home():
    """
    Renders the home page, displaying a list of books that can be sorted.
    """
    books_with_authors = []
    if "sort_by" in request.args.keys():
        sort_by = request.args["sort_by"]
        if sort_by == "title":
            books_with_authors = data_manager.get_all_books_with_authors_order_by_title()
        elif sort_by == "author":
            books_with_authors = data_manager.get_all_books_with_authors_order_by_authors()
        elif sort_by == "year":
            books_with_authors = data_manager.get_all_books_with_authors_order_by_publication_year()
        else:
            books_with_authors = data_manager.get_all_books_with_authors()
    else:
        books_with_authors = data_manager.get_all_books_with_authors()

    return render_template("home.html", books_with_authors=books_with_authors)


@app.route("/", methods=["POST"])
def home_post():
    """
    Handles the search form on the home page, filtering books by title.
    """
    title = request.form["title"]
    return render_template(
        "home.html", books_with_authors=data_manager.get_all_books_with_authors_by_title(title)
    )


@app.route("/delete/<int:book_id>", methods=["GET", "POST"])
def delete(book_id: int):
    """
    Deletes a book and redirects to the home page.
    """
    data_manager.delete_book_by_id(book_id)
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
    Handles the form submission for adding a new author.

    Returns:
        A tuple containing the rendered template and the HTTP status code.
    """
    name = request.form["name"]
    birth_date = request.form["birthdate"]
    date_of_death = request.form["date_of_death"]
    birth_date_dt = get_date_from_str(birth_date)
    date_of_death_dt = get_date_from_str(date_of_death)

    if data_manager.exist_author(name, birth_date, date_of_death):
        message = f"The author {name} with the birth date {get_date_print_format(birth_date_dt)} " + \
                  f"already exists!"
    elif date_of_death_dt is not None:
        if date_of_death_dt < birth_date_dt:
            message = \
                f"The author {name} date of death {get_date_print_format(date_of_death_dt)} " + \
                f"is before date of birth {get_date_print_format(birth_date_dt)}!"
    else:
        try:
            data_manager.add_Author(name, birth_date, date_of_death)
            message = f"The author {name} with the birth date {get_date_print_format(birth_date_dt)} " + \
                      f"has been added successfully!"
        except Exception as e:
            message = f"Error: {e}: The author {name} with the birth date {get_date_print_format(birth_date_dt)} " + \
                      f"has not been added!"
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
        authors=data_manager.get_all_authors(),
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
    author: Author = data_manager.get_author_by_id(author_id)

    if not is_isbn10(isbn) and not is_isbn13(isbn):
        message = f"The book {title} with ISBN: {isbn} is not valid!"
    elif data_manager.exist_book_isbn(isbn):
        message = f"The ISBN code: {isbn} already exists in the database!"
    elif data_manager.exist_book_by_autor_and_title(author_id, title):
        message = f"The book {title} form {author.name} already exists in the database!"
    else:
        try:
            data_manager.add_Book(isbn, title, publication_year, author_id)
            message = f"The book {title} form {author.name} has been added successfully!"
        except Exception as e:
            message = f"Error: {e}: The book {title} form {author.name}" + \
                      f"has not been added!"

    return (
        render_template(
            "add_book.html",
            authors=data_manager.get_all_authors(),
            visibility_book_message="",
            added_book_message=message,
        ),
        200,
    )


def create_database_tables(app: Flask) -> None:
    """
    Creates the database file and all tables defined in the models.

    This function must be called within the Flask application context.
    It includes error handling to catch and print any exceptions that
    occur during the database creation process.
    """
    print("Attempting to create database tables...")

    # db.create_all() MUST be called within the Flask Application Context
    # try/except block for robustness.
    try:
        with app.app_context():

            db.create_all()
            print("Database tables created or already exist.")

    except Exception as e:

        print(f"ERROR: Failed to create database tables. Reason: {e}")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        # Call the setup function to ensure the database file and tables are ready
        # This should be run at least once to initialize the tables, then comment it out.
        create_database_tables(app)

    app.run(host="0.0.0.0", port=5002, debug=True)
