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
        
def list_products(id):
    headers = ["Id", "Name", "Price", "Quantity", "Active"]
    data = database.get_products(id)

    print(tabulate(data, headers=headers, tablefmt="grid"))
