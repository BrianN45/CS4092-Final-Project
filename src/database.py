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
    product = Product(name=name, price=price, quantity=quantity, active=bool(active))
    query = """
    INSERT INTO
        Product (Name, Price, Quantity, Active)
    VALUES
        (?, ?, ?, ?)
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, product.to_db_tuple())
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
    INSERT INTO Inventory_Updates (
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


def get_products(id=0):
    query = "SELECT * FROM Product"
    params = ()

    if id != 0:
        query += " WHERE Id = ?"
        params = (id,)

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve products from system: {e}")
        return []

    return [Product.from_row(row) for row in rows]

def add_to_cart(customer_id, product_id, quantity):
    products = get_products(product_id)
    if not products:
        print(f"No product with an id of {product_id} was found.")
        return False

    product = products[0]
    if product.quantity < quantity:
        print(f"Not enough quantity for product with id {product_id}.")
        return False

    query = """
    INSERT INTO Cart (CustomerId, ProductId, Quantity)
    VALUES (?, ?, ?)
    ON CONFLICT(CustomerId, ProductId) DO UPDATE SET Quantity = Quantity + excluded.Quantity
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (int(customer_id), int(product_id), int(quantity)))
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Could not add product to cart: {e}")
        return False

    return True


def checkout_cart(customer_id, card_number):
    cart_items = get_cart_items(customer_id)
    if not cart_items:
        print("Your cart is empty.")
        return False

    for product_id, quantity, _ in cart_items:
        products = get_products(product_id)
        if not products:
            print(f"No product with an id of {product_id} was found.")
            return False
        if products[0].quantity < quantity:
            print(f"Not enough quantity for product with id {product_id}.")
            return False

    card_check_query = """
    SELECT 1
    FROM CreditCardCustomer
    WHERE CustomerId = ? AND CardNumber = ?
    """

    total_price = 0
    for _, quantity, unit_price in cart_items:
        total_price += quantity * unit_price

    purchase_query = """
    INSERT INTO Purchase (CustomerId, CardNumber, TotalPrice, PurchaseDate)
    VALUES (?, ?, ?, ?)
    """
    item_query = """
    INSERT INTO PurchasedItem (PurchaseId, ProductId, UnitPrice, Quantity)
    VALUES (?, ?, ?, ?)
    """
    update_query = "UPDATE Product SET Quantity = Quantity - ? WHERE Id = ?"
    clear_query = "DELETE FROM Cart WHERE CustomerId = ?"

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(card_check_query, (int(customer_id), str(card_number)))
            if cursor.fetchone() is None:
                print("Credit card is not associated with this customer.")
                return False

            cursor.execute(purchase_query, (int(customer_id), str(card_number), int(total_price), timestamp))
            purchase_id = cursor.lastrowid

            for product_id, quantity, unit_price in cart_items:
                cursor.execute(item_query, (purchase_id, int(product_id), int(unit_price), int(quantity)))
                cursor.execute(update_query, (int(quantity), int(product_id)))

            cursor.execute(clear_query, (int(customer_id),))
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Could not complete checkout: {e}")
        return False

    return True


def get_cart_items(customer_id):
    query = """
    SELECT c.ProductId, c.Quantity, p.Price
    FROM Cart c
    INNER JOIN Product p ON c.ProductId = p.Id
    WHERE c.CustomerId = ?
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (int(customer_id),))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve cart items: {e}")
        return []


def get_purchases(customer_id=None):
    query = """
    SELECT
        p.Id AS PurchaseId,
        p.CustomerId,
        p.CardNumber,
        p.TotalPrice,
        p.PurchaseDate,
        pr.Name AS ProductName,
        pi.Quantity,
        pi.UnitPrice
    FROM Purchase p
    LEFT JOIN PurchasedItem pi ON p.Id = pi.PurchaseId
    LEFT JOIN Product pr ON pi.ProductId = pr.Id
    """
    params = []

    if customer_id is not None:
        query += " WHERE p.CustomerId = ?"
        params.append(int(customer_id))

    query += " ORDER BY p.Id, pr.Id"

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve purchases: {e}")
        return []


def add_credit_card(customer_id, card_number, name, cvc, expiration_date, street_address, city, state, zip_code):
    credit_card = (card_number, name, cvc, expiration_date, street_address, city, state, zip_code)
    query = """
    INSERT INTO
        CreditCard (CardNumber, Name, CVC, ExpirationDate, StreetAddress, City, State, ZipCode)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
    """
    customerIDquery = """
    INSERT INTO
        CreditCardCustomer (CustomerId, CardNumber)
    VALUES
        (?, ?)
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, credit_card)
            if customer_id is not None:
                cursor.execute(customerIDquery, (int(customer_id), card_number))
    except sqlite3.Error as e:
        print(f"Could not add credit card into system: {e}")
        return False

    return True


def get_credit_cards(card_number = 0, customer_id = None):
    query = """
    SELECT cc.CardNumber, cc.Name, cc.CVC, cc.ExpirationDate, cc.StreetAddress, cc.City, cc.State, cc.ZipCode
    FROM CreditCard cc
    """
    params = []

    if customer_id is not None:
        query += """
        INNER JOIN CreditCardCustomer ccc
            ON cc.CardNumber = ccc.CardNumber
        WHERE ccc.CustomerId = ?
        """
        params.append(int(customer_id))

    if card_number != 0:
        if customer_id is None:
            query += " WHERE cc.CardNumber = ?"
        else:
            query += " AND cc.CardNumber = ?"
        params.append(str(card_number))

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            credit_cards = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Could not retrieve credit cards from system: {e}")
        return []

    return credit_cards


def get_customer_credit_cards(customer_id, card_number = 0):
    return get_credit_cards(card_number=card_number, customer_id=customer_id)

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
  
def edit_credit_card(customer_id, card_number, field, new_value, is_staff = False):

    query = f"UPDATE CreditCard SET {field} = ? WHERE CardNumber = ?"
    params = (new_value, str(card_number))

    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
    except sqlite3.Error as e:
        print(f"Could not update credit card in system: {e}")
        return False

    return True

