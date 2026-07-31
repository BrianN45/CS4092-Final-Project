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
            cli_helpers.list_products(int(arg))
        else:
            if arg != "":
                print(
                    "Invalid input, only whole numbers are allowed. Displaying all products instead."
                )
            cli_helpers.list_products(0)

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
        )
        print("\nAvailable commands for Customer:\n")
        print(
            "\nAvailable commands for either role:\n"
            "change - Change your role.\n"
            "view_cards - View all credit cards or a specific credit card.\n"
            "add_card - Add a new credit card.\n"
            "edit_card - Edit a credit card's details.\n"
            "remove_card - Remove a credit card from the system.\n"
            "view_products - View all products or a specific product.\n"
        )
