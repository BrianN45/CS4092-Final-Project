import sqlite3
from datetime import datetime
from pathlib import Path

from product import Product

DATABASE_NAME = "ecommerce.db"


def setup_database():
    setupPath = Path(__file__).resolve().parent / "queries" / "setup.sql"

    with open(setupPath, "r") as file:
        setup = file.read()

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.executescript(setup)
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Could not initiate setup: {e}")
        return False
        
    return True


def add_product(name, price, quantity, active):
    product = (name, price, quantity, active)
    query = """
    INSERT INTO
        Product (Name, Price, Quantity, Active)
    VALUES
        (?, ?, ?, ?)
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, product)
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Could not add product into system: {e}")
        return False

    return True


def edit_product(staffId, productId, price, quantity, active):
    result = get_products(productId)

    if len(result) == 0:
        print(f"No product with an id of {productId} was found.")
        return False

    product = result[0]

    # Check if quantity is below 0
    if product.quantity + quantity < 0:
        print("New quantity is below 0.")
        return False

    new_price = product.price if price is None else price
    new_quantity = product.quantity if quantity is None else product.quantity + quantity
    new_active = product.active if active is None else bool(active)

    updates = []
    updateParams = []

    if price is not None:
        updates.append("Price = ?")
        updateParams.append(price)

    if quantity is not None:
        updates.append("Quantity = ?")
        updateParams.append(quantity + product.quantity)

    if active is not None:
        updates.append("Active = ?")
        updateParams.append(int(new_active))

    if not updates:
        print("No changes made.")
        return False

    updateParams.append(int(productId))
    updateQuery = f"UPDATE Product SET {', '.join(updates)} WHERE Id = ?"

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")
    logQuery = """
    INSERT INTO InventoryUpdates (
        Staff_Id,
        Product_Id,
        Date_Updated,
        Old_Price,
        New_Price,
        Quantity_Change,
        New_Quantity,
        Active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    logParams = (
        int(staffId),
        int(productId),
        timestamp,
        product.price * 100,
        new_price,
        quantity,
        new_quantity,
        int(new_active),
    )

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(updateQuery, updateParams)
            cursor.execute(logQuery, logParams)
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Could not update product in system: {e}")
        return False

    return True


def get_products(id=0, active=False):
    query = "SELECT * FROM Product"
    params = ()

    if id != 0:
        query += " WHERE Id = ?"
        
        # Show active products only
        if active:
            query += " AND Active = 1"
        params = (id,)
    elif active:
        query += " WHERE Active = 1"
    

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve products from system: {e}")
        return []

    return [Product.from_row(row) for row in rows]


def add_credit_card(card_number, name, cvc, expiration_date, street_address, city, state, zip_code):
    credit_card = (card_number, name, cvc, expiration_date, street_address, city, state, zip_code)
    query = """
    INSERT INTO
        CreditCard (CardNumber, Name, CVC, ExpirationDate, StreetAddress, City, State, ZipCode)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, credit_card)
    except sqlite3.Error as e:
        print(f"Could not add credit card into system: {e}")
        return False

    return True


def get_credit_cards(card_number = 0):
    query = "SELECT * FROM CreditCard"

    params = ()

    if card_number != 0:
        query += " WHERE CardNumber = ?"
        params = (card_number,)

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            credit_cards = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve credit cards from system: {e}")
        return []

    return credit_cards

def get_customers(id = 0):
    query = "SELECT * FROM Customer"
    params = ()
    
    if id != 0:
        query += " WHERE Id = ?"
        params = (id,)
        
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            customers = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve customers from system: {e}")
        return []

    return customers

def get_staff(id = 0):
    query = "SELECT * FROM Staff"
    params = ()
    
    if id != 0:
        query += " WHERE Id = ?"
        params = (id,)
        
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            staff = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve staff from system: {e}")
        return []

    return staff
  
def edit_credit_card(card_number, field, new_value):
    query = f"UPDATE CreditCard SET {field} = ? WHERE CardNumber = ?"
    params = (new_value, card_number)

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
    except sqlite3.Error as e:
        print(f"Could not update credit card in system: {e}")
        return False

    return True

