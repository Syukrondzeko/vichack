import os
import sqlite3
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

DB_URL = f"{os.path.dirname(os.path.abspath(__file__))}/database/restaurant.db"

def create_tables_and_populate():
    # Create connection
    with sqlite3.connect(DB_URL) as connection:

        # Create tables
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS menu (
                menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_name TEXT NOT NULL UNIQUE,
                price DOUBLE NOT NULL
            );
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT
            );
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER,
                quantity TEXT,
                status TEXT,

                FOREIGN KEY(menu_id) REFERENCES menu(menu_id)
            );
            """
        )

        # Insert menus
        connection.execute(
            """
            INSERT INTO menu VALUES
            (NULL, "cheesecake", 6.99),
            (NULL, "beef burgers", 12.99),
            (NULL, "fried noodle", 9.99),
            (NULL, "meatball soup", 7.99),
            (NULL, "chicken teriyaki", 11.99),
            (NULL, "sambal chicken wings", 8.99),
            (NULL, "grilled fish", 10.99),
            (NULL, "katsu curry", 13.99),
            (NULL, "mixed rice bowl", 9.99),
            (NULL, "veggie pizza", 14.99);
            """
        )

        connection.execute(
            """
            INSERT INTO user VALUES (NULL);
            """
        )

        connection.commit()

def drop_all() -> None:
    with sqlite3.connect(DB_URL) as connection:
        connection.execute(
            """
            DROP TABLE IF EXISTS menu;
            """
        )
        connection.execute(
            """
            DROP TABLE IF EXISTS user;
            """
        )
        connection.execute(
            """
            DROP TABLE IF EXISTS orders;
            """
        )

def init_db() -> None:
    # Create file if it doesn't exists
    open(DB_URL, "w")
    drop_all()
    create_tables_and_populate()

if __name__ == "__main__":
    init_db()
