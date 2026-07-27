import sqlite3
from pathlib import Path

databaseName = "ecommerce.db"


def setup_database():
    setupPath = Path(__file__).resolve().parent / "queries" / "setup.sql"

    with open(setupPath, "r") as file:
        setup = file.read()

    try:
        with sqlite3.connect(databaseName) as connection:
            cursor = connection.cursor()
            cursor.executescript(setup)
    except sqlite3.Error as e:
        print(f"Could not initiate setup: {e}")


def add_product(name, price, quantity, active):
    product = (name, price, quantity, active)
    query = """
    INSERT INTO
        Product (Name, Price, Quantity, Active)
    VALUES
        (?, ?, ?, ?)
    """

    try:
        with sqlite3.connect(databaseName) as connection:
            cursor = connection.cursor()
            cursor.execute(query, product)
    except sqlite3.Error as e:
        print(f"Could not add product into system: {e}")
        return False
    
    return True
