from ast import arg
import cmd

import cli_helpers

DEFAULT_CUSTOMER_ID = 1 ## CHANGE THIS ##

commands = {"staff": ["add", "edit", "remove", "change", "view_products"], "customer": ["change", "view_products"]}

def convert(type, value):
    try:
        type(value)
        return True
    except (ValueError, TypeError):
        return False

class Interactive(cmd.Cmd):
    intro = "Welcome to the Super Awesome Store! You are currently a customer.\nType help to see the list of commands.\n"
    prompt = "\nEnter a command: "
    isStaff = False
    customerId = DEFAULT_CUSTOMER_ID

    def do_change(self, arg):
        """
        Usage: change

        Changes your role. The available roles are Staff Member and Customer.
        """
        self.isStaff = not self.isStaff
        print(f"You are now a {'Staff Member' if self.isStaff else 'Customer'}.")
        
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
            print("Invalid input, only whole numbers are allowed. Displaying all products instead.")
            cli_helpers.list_products(0)

    def do_add(self, arg):
        """
        Usage: add

        Add a product into a system.
        """
        if not self.isStaff:
            print("You are not a staff member.")
            return

        cli_helpers.add_product()

    def do_edit(self, arg):
        """
        Usage: edit <product id>

        Edit a product's quantity and price.

        Arguments:
            <product id> - The id of the product. You can get the list of products using "insert command here"
        """

    def do_remove(self, arg):
        """
        Usage: remove <product id>

        Remove a product from the system.

        Arguments:
            <product id> - The id of the product. You can get the list of products using "insert command here"
        """

    def do_view_cards(self, arg):
        """
        Usage: view_cards <credit card number>

        Displays all credit cards in the system, or a specific credit card if a number is provided.
            
        Arguments:
            <credit card number> - The number of the credit card. If no number is provided, all credit cards will be displayed.
        """
        if convert(int, arg) and arg != "":
            cli_helpers.list_credit_cards(int(arg))
        else:
            print("Invalid input, only whole numbers are allowed. Displaying all credit cards instead.")
            cli_helpers.list_credit_cards(0)

    def do_add_card(self, arg):
        """
        Usage: add card

        Add a credit card into the system.
        """

        cli_helpers.add_credit_card()

    def do_edit_card(self, arg):
        """
        Usage: edit <card number>

        Edit a credit card's details.

        Arguments:
            <card number> - The number of the credit card. You can get the list of credit cards using "insert command here"
        """

    def do_remove_card(self, arg):
        """
        Usage: remove <card number>

        Remove a credit card from the system.

        Arguments:
            <card number> - The number of the credit card. You can get the list of credit cards using "insert command here"
        """

    def do_exit(self, arg):
        """Exits the application."""
        print("Exiting application.")
        return True

    def do_help(self, arg):
        role = "staff" if self.isStaff else "customer"

        if arg:
            if arg.lower() in commands[role]:
                super().do_help(arg)
                return
            else:
                print(
                    f"Command for {arg} not found. Listing all commands for your role."
                )

        if self.isStaff:
            print(
                "\nAvailable commands for Staff:\n"
                "add - Add a new product.\n"
                "edit - Edit a product's quantity and price.\n"
                "remove - Removes a product.\n"
                "change - Change your role.\n"
                "view_products - View all products or a specific product.\n"
            )
        else:
            print("\nAvailable commands for Customer:\n"
                  "change - Change your role.\n"
                  "view_products - View all products or a specific product.\n"
                  "add_card - Add a new credit card.\n"
                  "view_cards - View all credit cards or a specific credit card.\n"
                  "edit_card - Edit a credit card's details.\n"
                  "remove_card - Remove a credit card from the system.\n"
            )
