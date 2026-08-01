import re

from tabulate import tabulate

import database


def get_input(prompt, pattern, error):
    while True:
        user_input = input(prompt)

        if re.fullmatch(pattern, user_input):
            return user_input

        print(error)


def add_product():
    name = get_input(
        "Name of the product: ",
        r"^[a-zA-Z]+$",
        "Invalid input, only alphabetic characters are allowed.",
    )

    price = get_input(
        "Price of the product: ",
        r"^\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?$",
        "Invalid input, examples of valid inputs are 50, 12.99, and 1,032.",
    )
    price = price * 100

    quantity = get_input(
        "Quantity of the product: ",
        r"^\d+$",
        "Invalid input, only whole numbers are allowed.",
    )

    active = get_input(
        "Should the product be listed? (Y/N): ",
        r"^[YN]$",
        "Invalid input, only Y and N are allowed.",
    )
    active = 1 if active == "Y" else 0

    successful = database.add_product(name, price, quantity, active)

    if successful:
        print(f"Added {name} into the system.")
    else:
        print(f"{name} was not added to the system.")


def edit_product(staffid, productId):
    headers = ["Id", "Name", "Price", "Quantity", "Active", "Rating"]
    result = database.get_products(productId)

    if len(result) == 0:
        print(f"No product with an id of {productId} was found.")
        return

    display_rows = [
        [item.id, item.name, item.price, item.quantity, item.active, item.rating]
        for item in result
    ]

    print("Information about product:")
    print(tabulate(display_rows, headers=headers, tablefmt="grid"))
    print("Enter changes, leave empty if no change needed.")

    price_input = get_input(
        "New price of the product: ",
        r"^(?:\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})|)$",
        "Invalid input, examples of valid inputs are 50, 12.99, and 1,032. It can also be empty.",
    )

    quantity_input = get_input(
        "Quantity of the product (this will add or subtract the current quantity): ",
        r"^(?:-?\d+|)$",
        "Invalid input, only whole numbers are allowed. It can also be empty.",
    )

    active_input = get_input(
        "Should the product be listed? (Y/N): ",
        r"^(?:[YN]|)$",
        "Invalid input, only Y and N are allowed. It can also be empty.",
    )

    if not price_input and not quantity_input and not active_input:
        print("No changes made.")
        return

    price = int(price_input) * 100 if price_input else None
    quantity = int(quantity_input) if quantity_input else None
    active = 1 if active_input == "Y" else 0 if active_input == "N" else None

    successful = database.edit_product(staffid, productId, price, quantity, active)

    if successful:
        print("Product updated successfully.")
    else:
        print("Product was not updated.")


def buy_product(customer_id, product_id, quantity):
    successful = database.add_to_cart(customer_id, product_id, quantity)

    if successful:
        print(f"Added {quantity} of product with id {product_id} to your cart.")
    else:
        print(f"Could not add product with id {product_id} to your cart.")


def view_cart(customer_id):
    data = database.get_cart_items(customer_id)

    if not data:
        print("Your cart is empty.")
        return

    headers = ["Product ID", "Quantity", "Unit Price"]
    display_rows = [
        [product_id, quantity, unit_price/100]
        for product_id, quantity, unit_price in data
    ]
    print(tabulate(display_rows, headers=headers, tablefmt="grid"))


def view_purchases(customer_id=None, is_staff=False):
    data = database.get_purchases(customer_id=customer_id if not is_staff else None)

    if not data:
        print("No purchases found.")
        return

    headers = [
        "Purchase ID",
        "Customer ID",
        "Card Number",
        "Total Price",
        "Purchase Date",
        "Product",
        "Quantity",
        "Unit Price",
    ]
    display_rows = [
        [
            purchase_id,
            customer_id,
            card_number,
            total_price/100,
            purchase_date,
            product_name,
            quantity,
            unit_price/100,
        ]
        for purchase_id, customer_id, card_number, total_price, purchase_date, product_name, quantity, unit_price in data
    ]

    print(tabulate(display_rows, headers=headers, tablefmt="grid"))


def checkout(customer_id, card_number):
    successful = database.checkout_cart(customer_id, card_number)

    if successful:
        print("Checkout completed successfully.")
    else:
        print("Checkout failed.")


def list_purchases(customer_id=None, is_staff=False):
    headers = ["Purchase ID", "Customer ID", "Purchase Date"]
    data = database.get_purchases(customer_id=customer_id if not is_staff else None)

    if not data:
        print("No purchases found.")
        return

    print(tabulate(data, headers=headers, tablefmt="grid"))


def list_products(id, active=False):
    headers = ["Id", "Name", "Price", "Quantity", "Active", "Rating"]
    data = database.get_products(id, active)

    if len(data) == 0:
        print("No products found.")
        return False

    display_rows = [
        [item.id, item.name, item.price, item.quantity, item.active, item.rating]
        for item in data
    ]

    print(tabulate(display_rows, headers=headers, tablefmt="grid"))
    return True


def add_credit_card(customer_id=None, is_staff=False):
    if customer_id is None and not is_staff:
        print("You must be logged in as a customer to add a credit card.")
        return False

    card_number = get_input(
        "Credit card number: ",
        r"^\d{16}$",
        "Invalid input, only 16-digit numbers are allowed.",
    )

    name = get_input(
        "Name on the credit card: ",
        r"^[a-zA-Z0-9\s]+$",
        "Invalid input, only alphabetic characters are allowed.",
    )

    cvc = get_input(
        "CVC: ",
        r"^\d{3}$",
        "Invalid input, only 3-digit numbers are allowed.",
    )

    expiry = get_input(
        "Expiry date (MM/YY): ",
        r"^\d{2}/\d{2}$",
        "Invalid input, examples of valid inputs are 12/23 and 01/24.",
    )

    street_address = get_input(
        "Street address: ",
        r"^[a-zA-Z0-9\s]+$",
        "Invalid input, only alphanumeric characters and spaces are allowed.",
    )

    city = get_input(
        "City: ",
        r"^[a-zA-Z\s]+$",
        "Invalid input, only alphabetic characters and spaces are allowed.",
    )

    state = get_input(
        "State (2-letter abbreviation): ",
        r"^[A-Z]{2}$",
        "Invalid input, only 2 uppercase letters are allowed.",
    )

    zip_code = get_input(
        "ZIP code: ",
        r"^\d{5}$",
        "Invalid input, only 5-digit numbers are allowed.",
    )

    successful = database.add_credit_card(
        customer_id,
        card_number,
        name,
        cvc,
        expiry,
        street_address,
        city,
        state,
        zip_code,
    )

    if successful:
        print(f"Added {name}'s credit card into the system.")
    else:
        print(f"{name}'s credit card was not added to the system.")

    return successful


def list_credit_cards(card_number, customer_id=None, is_staff=False):
    headers = [
        "Card Number",
        "Name",
        "CVC",
        "Expiration Date",
        "Street Address",
        "City",
        "State",
        "ZIP Code",
    ]
    data = database.get_credit_cards(
        card_number=card_number, customer_id=customer_id if not is_staff else None
    )

    if not data:
        print("No credit cards found.")
        return

    print(tabulate(data, headers=headers, tablefmt="grid"))


def change_role(cli, role):
    if role == "staff":
        data = database.get_staff()

        headers = ["Id", "Name"]
        print("Table of available staff members:")
        print(tabulate(data, headers=headers, tablefmt="grid"))

        id = get_input(
            "Id of staff: ",
            r"^[0-9]+$",
            "Invalid input, only whole numbers are allowed.",
        )

        staff = database.get_staff(id)

        if len(staff) == 0:
            print(f"Staff member with an id of {id} was not found.")
            return False

        headers = ["Id", "Name"]
        print("Changing to the staff member below...")
        print(tabulate(staff, headers=headers, tablefmt="grid"))

        cli.isStaff = True
        cli.staffId = int(staff[0][0])

        return True

    if role == "customer":
        data = database.get_customers()

        headers = ["Id", "Name", "DoB", "StreetAddress", "City", "State", "ZipCode"]
        print("Table of available customers:")
        print(tabulate(data, headers=headers, tablefmt="grid"))

        id = get_input(
            "Id of customer: ",
            r"^[0-9]+$",
            "Invalid input, only whole numbers are allowed.",
        )

        customer = database.get_customers(id)

        if len(customer) == 0:
            print(f"Customer with an id of {id} was not found.")
            return False

        headers = ["Id", "Name"]
        print("Changing to the customer below...")
        print(tabulate(customer, headers=headers, tablefmt="grid"))

        cli.isStaff = False
        cli.customerId = int(customer[0][0])

        return True

    return False


def edit_credit_card(customer_id, card_number, field, is_staff=False):
    valid_fields = [
        "Name",
        "CVC",
        "ExpirationDate",
        "StreetAddress",
        "City",
        "State",
        "ZipCode",
    ]
    if field not in valid_fields:
        print(f"Invalid field name. Valid fields are: {', '.join(valid_fields)}")
        return

    new_value = get_input(
        f"Enter new value for {field}: ",
        r"^[a-zA-Z0-9\s]+$",
        "Invalid input, only alphanumeric characters and spaces are allowed.",
    )

    successful = database.edit_credit_card(
        customer_id, card_number, field, new_value, is_staff
    )

    if successful:
        print(f"Updated {field} for credit card {card_number}.")
    else:
        print(f"Failed to update {field} for credit card {card_number}.")

    return successful


def rate_product(customerId, productId):
    print(f"Listing product with an id of {productId}")
    products = list_products(productId)

    if not products:
        return False

    rating = get_input(
        "How would you rate the product from 0 to 5? ",
        r"^[0-5]$",
        "Invalid input, only whole numbers from 0 to 5 are allowed.",
    )

    description = get_input(
        "Why do you rate it that way? ",
        r".+",
        "",
    )

    return database.rate_product(customerId, productId, rating, description)


def view_product_ratings(productId):
    product = database.get_products(productId)

    if len(product) == 0:
        print(f"No product with an id of {productId} was found.")
        return False

    ratings = database.get_product_ratings(productId)

    if len(ratings) == 0:
        print(f"No ratings found for product with an id of {productId}.")
        return False

    headers = ["Customer Name", "Product Name", "Rate", "Description"]
    print(tabulate(ratings, headers=headers, tablefmt="grid"))
    return True

def view_product_history(product_id):
    product = database.get_products(product_id)

    if len(product) == 0:
        print(f"No product with an id of {product_id} was found.")
        return False

    data = database.get_inventory_updates(product_id)

    if len(data) == 0:
        print(f"No inventory history found for product with an id of {product_id}.")
        return False

    headers = [
        "Staff ID",
        "Product ID",
        "Date Updated",
        "Old Price",
        "New Price",
        "Quantity Change",
        "New Quantity",
        "Active",
    ]
    display_rows = [
        [
            staff_id,
            product_id,
            date_updated,
            old_price/100,
            new_price/100,
            quantity_change,
            new_quantity,
            "Yes" if active else "No",
        ]
        for staff_id, product_id, date_updated, old_price, new_price, quantity_change, new_quantity, active in data
    ]

    print(tabulate(display_rows, headers=headers, tablefmt="grid"))
    return True