from database import setup_database
from cli import Interactive

if __name__ == "__main__":
    print("Running application.")
    setup_database()
    Interactive().cmdloop()