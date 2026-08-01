import cmd

import cli_helpers

DEFAULT_STAFF_ID = 1
DEFAULT_CUSTOMER_ID = 1
commands = [
    "add_product",
    "edit_product",
    "remove_product",
    "change",
    "view_products",
    "view_cards",
    "add_card",
    "edit_card",
    "remove_card",
]


def convert(type, value):
    try:
        type(value)
        return True
    except (ValueError, TypeError):
        return False


class Interactive(cmd.Cmd):
    intro = "Welcome to the Super Awesome Store! You are currently logged in as Brian as a Customer.\nType help to see the list of commands.\n"
    prompt = "\nEnter a command: "
    isStaff = False
    staffId = DEFAULT_STAFF_ID
    customerId = DEFAULT_CUSTOMER_ID

    def do_change(self, arg):
        """
        Usage: change <customer/staff>

        Changes your role. The available roles are Staff Member and Customer.

        Arguments:
            <customer/staff>: Either "customer" or "staff," you will be prompted to enter an id afterwards.
        """
        role = arg.strip().lower() if arg else ""
        if role not in {"customer", "staff"}:
            print("Please enter a role: customer or staff.")
            return

        success = cli_helpers.change_role(self, role)

        if success:
            print(f"You are now a {'staff member' if self.isStaff else 'customer'}.")
        else:
            print("Role change unsuccessful.")

    def do_view_products(self, arg):
        """
        Usage: view_products <product id>

        Displays all products in the system, or a specific product if an id is provided.

        Arguments:
            <product id> - The id of the product. If no id is provided, all products will be displayed.
        """
        if convert(int, arg) and arg != "":
            cli_helpers.list_products(int(arg), not self.isStaff)
        else:
            if arg != "":
                print(
                    "Invalid input, only whole numbers are allowed. Displaying all products instead."
                )
            cli_helpers.list_products(0, not self.isStaff)

    def do_add_product(self, arg):
        """
        Usage: add_product

        Add a product into a system.
        """
        if not self.isStaff:
            print("You are not a staff member.")
            return

        cli_helpers.add_product()

    def do_edit_product(self, arg):
        """
        Usage: edit_product <product id>

        Edit a product's quantity and price, or delist it from the store.

        Arguments:
            <product id> - The id of the product.
        """
        if not self.isStaff:
            print("You are not a staff member.")
            return

        if convert(int, arg) and arg != "":
            cli_helpers.edit_product(self.staffId, arg)
        else:
            print("Invalid input, only product ids are allowed.")

    def do_buy_product(self, arg):
        """
        Usage: buy_product <product id> <quantity>

        Add a product to the customer's cart.

        Arguments:
            <product id> - The id of the product.
            <quantity> - The quantity of the product to add to the cart.
        """
        if self.isStaff:
            print("You are not a customer.")
            return

        args = arg.split()
        if len(args) != 2 or not all(convert(int, a) for a in args):
            print("Invalid input, please provide a product id and quantity.")
            return

        product_id, quantity = map(int, args)
        cli_helpers.buy_product(self.customerId, product_id, quantity)

    def do_view_cart(self, arg):
        """
        Usage: view_cart

        Display the products currently in the customer's cart.
        """
        if self.isStaff:
            print("You are not a customer.")
            return

        cli_helpers.view_cart(self.customerId)

    def do_view_purchases(self, arg):
        """
        Usage: view_purchases

        Display the current customer's purchase history.
        """
        if self.isStaff:
            cli_helpers.view_purchases(is_staff=True)
            return

        cli_helpers.view_purchases(self.customerId, is_staff=False)

    def do_checkout(self, arg):
        """
        Usage: checkout <credit card number>

        Complete the purchase for all products currently in the cart.
        """
        if self.isStaff:
            print("You are not a customer.")
            return

        if not arg or not convert(int, arg):
            print("Invalid input, please provide a credit card number.")
            return

        cli_helpers.checkout(self.customerId, int(arg))

    def do_view_cards(self, arg):
        """
        Usage: view_cards <credit card number>

        Displays all credit cards in the system, or a specific credit card if a number is provided.

        Arguments:
            <credit card number> - The number of the credit card. If no number is provided, all credit cards will be displayed.
        """
        if convert(int, arg) and arg != "":
            cli_helpers.list_credit_cards(
                int(arg),
                self.customerId if not self.isStaff else None,
                self.isStaff,
            )
        else:
            if arg != "":
                print(
                    "Invalid input, only whole numbers are allowed. Displaying all credit cards instead."
                )
            cli_helpers.list_credit_cards(
                0,
                self.customerId if not self.isStaff else None,
                self.isStaff,
            )

    def do_add_card(self, arg):
        """
        Usage: add card

        Add a credit card into the system.
        """
        cli_helpers.add_credit_card(
            self.customerId if not self.isStaff else None,
            self.isStaff,
        )

    def do_edit_card(self, arg):
        """
        Usage: edit <card number>

        Edit a credit card's details.

        Arguments:
            <card number> - The number of the credit card. You can get the list of credit cards using "insert command here"
        """
        if convert(int, arg) and arg != "":
            cli_helpers.list_credit_cards(
                int(arg),
                self.customerId if not self.isStaff else None,
                self.isStaff,
            )
            print("which field would you like to edit?")
            field = input("Enter the field name: ")
            cli_helpers.edit_credit_card(
                self.customerId if not self.isStaff else None,
                int(arg),
                field,
                self.isStaff,
            )
        else:
            print("Credit card not found. Displaying all credit cards instead.")
            cli_helpers.list_credit_cards(
                0,
                self.customerId if not self.isStaff else None,
                self.isStaff,
            )

    def do_rate_product(self, arg):
        """
        Usage: rate_product <product id>

        Rate a product.

        Arguments:
            <product id>: Id of the product.
        """
        if self.isStaff:
            print("You are not a customer.")
            return

        if convert(int, arg) and arg != "":
            successful = cli_helpers.rate_product(self.customerId, int(arg))

            if not successful:
                print(f"Failed to rate product with an id of {arg}.")
            else:
                print("Successfully rated product!")
        else:
            print("Invalid input, only whole numbers are allowed.")

    def do_view_product_rating(self, arg):
        """
        Usage: view_product_rating <product id>

        View all ratings for a product.

        Arguments:
            <product id>: Id of the product.
        """
        if convert(int, arg) and arg != "":
            successful = cli_helpers.view_product_ratings(int(arg))

            if not successful:
                print(f"Failed to get product ratings for a product id of {arg}.")
        else:
            print("Invalid input, only whole numbers are allowed.")

    def do_exit(self, arg):
        """Exits the application."""
        print("Exiting application.")
        return True

    def do_help(self, arg):
        if arg:
            if arg.lower() in commands:
                super().do_help(arg)
                return
            else:
                print(f"Command for {arg} not found. Listing all commands.")


        print(
            "\nAvailable commands for Staff:\n"
            "add_product - Add a new product.\n"
            "edit_product - Edit a product's quantity and price, or delist it from the store.\n"
          
            "\nAvailable commands for Customer:\n"
            "view_cards - View all credit cards or a specific credit card.\n"
            "add_card - Add a new credit card.\n"
            "edit_card - Edit a credit card's details.\n"
            "buy_product [product_id] [quantity] - Add a product to your cart.\n"
            "view_cart - View the products currently in your cart.\n"
            "view_purchases - View your purchase history.\n"
            "checkout [card_number] - Checkout the current cart and create a purchase.\n"
          
            "\nAvailable commands for either role:\n"
            "change - Change your role.\n"
            "view_products - View all products or a specific product.\n"
            "view_product_rating - Shows a product's rating\n"
        )
