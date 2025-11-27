# BookAlchemy

BookAlchemy is a simple web application for managing a library of books and authors. It is built with Python, Flask, and SQLAlchemy.

## Project Structure

- `app.py`: The main application file. It contains the Flask routes and the logic for handling requests.
- `data_models.py`: Defines the database models for a book and an author using SQLAlchemy.
- `static/`: Contains the static files for the web application.
    - `style.css`: The main stylesheet for the application.
    - `add_style.css`: The stylesheet for the "add" pages.
    - `book_cover_form_google_api.js`: A Javascript file for fetching book covers from the Google Books API.
- `templates/`: Contains the HTML templates for the web application.
- `data/`: Contains the SQLite database file.

## Setup

1. **Install the dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```
   python app.py
   ```

The application will be available at `http://127.0.0.1:5000`.
