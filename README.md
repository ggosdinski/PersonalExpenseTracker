# PersonalExpenseTracker
# Overview

This project is a personal expense tracker built in Python that integrates with a SQLite relational database. The goal of this software is to deepen my skills in software development by designing a real-world application that handles data storage, processing, and retrieval using Python and SQL. It allows users to manage their financial records by categorizing expenses, adding and editing transactions, and generating analytical reports based on spending patterns.

The application provides a command-line interface where users can:
- Create and manage expense categories.
- Add, view, update, and delete financial transactions.
- Analyze total expenses by category and date range.
- Maintain organized and persistent financial data using SQLite.

My purpose for developing this project is to practice integrating Python with a relational database system, understand database schema design, and strengthen my ability to write modular and maintainable code.

[Software Demo Video]
(https://youtu.be/7_-jq4EMWX0)

# Relational Database

This project uses a SQLite relational database to persist data. SQLite was chosen for its simplicity and ease of integration with Python, especially for small-scale, personal applications.

The database contains two primary tables:

1. **Categories**
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `name` (TEXT NOT NULL)

2. **Transactions**
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `category_id` (INTEGER NOT NULL, FOREIGN KEY to Categories)
   - `amount` (REAL NOT NULL)
   - `date` (TEXT NOT NULL)
   - `description` (TEXT)

The relationship is one-to-many: each category can be associated with multiple transactions, but each transaction belongs to only one category.

# Development Environment

The software was developed using the following tools and technologies:

- **Operating System:** Windows 11
- **Code Editor:** Visual Studio Code
- **Database:** SQLite
- **Programming Language:** Python 3.12

### Libraries used:
- `sqlite3` – for database interactions
- `datetime` – for handling and formatting dates
- `os` – for console screen clearing and user experience enhancement

# Useful Websites

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python SQLite3 Module](https://docs.python.org/3/library/sqlite3.html)
- [Real Python - Working with SQLite](https://realpython.com/python-sqlite-sqlalchemy/)
- [W3Schools - Python SQLite](https://www.w3schools.com/sql/sql_python.asp)

# Future Work

- Add user authentication to support multiple users with separate databases.
- Implement a GUI using Tkinter or a web-based interface with Flask.
- Add monthly/weekly spending summary reports and visualizations using Matplotlib.
- Export data to CSV or Excel for further analysis.
- Add input validation and error handling to enhance user experience and stability.
