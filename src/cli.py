import cmd

import cli_helpers

commands = {"staff": ["add", "edit", "remove", "change"], "customer": ["change"]}

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
                "change - Change your role."
            )
        else:
            print("\nAvailable commands for Customer:\nchange - Change your role.")
