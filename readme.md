# BooksWithSQLAlchemy

BookAlchemy is a simple web application for managing a library of books and authors. It is built with Python, Flask, and SQLAlchemy.

## Features

- List all books and authors.
- Add new books and authors.
- Delete books.
- Search for books by title.
- Sort books by title, author, or publication year.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- HTML
- CSS
- JavaScript

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/BooksWithSQLAlchemy.git
   ```

2. **Navigate to the project directory:**
   ```
   cd BooksWithSQLAlchemy
   ```

3. **Install the dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

The application will be available at `http://127.0.0.1:5002`.

## Usage

- The home page displays a list of all books in the library.
- You can sort the books by clicking on the column headers.
- To add a new book or author, click on the "Add Book" or "Add Author" buttons.
- To delete a book, click on the "Delete" button next to the book.
- To search for a book, use the search bar on the home page.

## Project Structure

- `app.py`: The main application file. It contains the Flask routes and the logic for handling requests.
- `data_manager.py`: A data access layer that provides an interface for interacting with the database.
- `data_models.py`: Defines the database models for a book and an author using SQLAlchemy.
- `static/`: Contains the static files for the web application.
    - `style.css`: The main stylesheet for the application.
    - `add_style.css`: The stylesheet for the "add" pages.
    - `book_cover_form_google_api.js`: A Javascript file for fetching book covers from the Google Books API.
- `templates/`: Contains the HTML templates for the web application.
- `data/`: Contains the SQLite database file.
