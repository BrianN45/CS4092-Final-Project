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


def add_credit_card():
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

    successful = database.add_credit_card(card_number, name, cvc, expiry, street_address, city, state, zip_code)

    if successful:
        print(f"Added {name}'s credit card into the system.")
    else:
        print(f"{name}'s credit card was not added to the system.")

def list_credit_cards(card_number):
    headers = ["Card Number", "Name", "CVC", "Expiration Date", "Street Address", "City", "State", "ZIP Code"]
    data = database.get_credit_cards(card_number)

    print(tabulate(data, headers=headers, tablefmt="grid"))
        
