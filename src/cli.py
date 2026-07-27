import cmd
import database
import re

commands = {"staff": ["add", "edit", "remove", "change"], "customer": ["change"]}


def get_input(prompt, pattern, error):
    while True:
        user_input = input(prompt)

        if re.fullmatch(pattern, user_input):
            return user_input

        print(error)


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

    def do_add(self, arg):
        """
        Usage: add

        Add a product into a system.
        """
        if not self.isStaff:
            print("You are not a staff member.")
            return

        name = get_input(
            "Name of the product: ",
            r"^[a-zA-Z]+$",
            "Invalid input, only alphabetic characters are allowed.",
        )

        priceStr = get_input(
            "Price of the product: ",
            r"^\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?$",
            "Invalid input, examples of valid inputs are 50, 12.99, and 1,032.",
        )
        price = float(priceStr.replace(",", ""))

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

        successful = database.add_product(name, price, quantity, active)

        if successful:
            print(f"Added {name} into the system.")
        else:
            print(f"{name} was not added to the system.")

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
            print("\nAvailable commands for Customer:\n" \
            "change - Change your role.")
