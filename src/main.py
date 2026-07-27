from cli import Interactive
from database import setup_database

if __name__ == "__main__":
    print("Running application.")
    setup_database()
    Interactive().cmdloop()
