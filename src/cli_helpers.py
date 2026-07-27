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
    price = float(price.replace(",", ""))

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
    headers = ["Id", "Name", "Price", "Quantity", "Active"]
    result = database.get_products(productId)
    
    if len(result) == 0:
        print(f"No product with an id of {productId} was found.")
        return

    print("Information about product:")
    print(tabulate(result, headers=headers, tablefmt="grid"))
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

    price = float(price_input.replace(",", "")) * 100 if price_input else None
    quantity = int(quantity_input) if quantity_input else None
    active = 1 if active_input == "Y" else 0 if active_input == "N" else None

    successful = database.edit_product(staffid, productId, price, quantity, active)

    if successful:
        print("Product updated successfully.")
    else:
        print("Product was not updated.")


def list_products(id):
    headers = ["Id", "Name", "Price", "Quantity", "Active"]
    data = database.get_products(id)

    print(tabulate(data, headers=headers, tablefmt="grid"))