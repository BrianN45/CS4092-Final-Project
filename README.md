# E-Commerce CLI Project

A command-line shopping system for that supports customers, staff, products, carts, checkout, purchases, and credit card management.

## Install Dependencies

Run the following command to install required Python libraries:

```bash
pip install -r requirements.txt
```

## Run the Application

From the project root directory, start the CLI with:

```bash
python src/main.py
```

Then use the available commands to browse products, add items to the cart, checkout, and view purchase history.

## Available Commands

- `change <customer/staff>`: Change the current role between customer and staff.
- `view_products [product id]`: List all products or a specific product.
- `add_product`: Add a new product (staff only).
- `edit_product <product id>`: Edit product price, quantity, or active status (staff only).
- `view_cards [credit card number]`: View all credit cards or a specific credit card.
- `add_card`: Add a new credit card.
- `edit_card <card number>`: Edit a credit card's details.
- `rate_product <product id>`: Rate a product (customer only).
- `view_product_rating <product id>`: View ratings for a product.
- `exit`: Exit the application.

## ER Diagram
![ER Diagram](ERDiagram.png)
