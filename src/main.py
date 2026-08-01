from cli import Interactive
from database import setup_database

if __name__ == "__main__":
    print("Running application.")
    successful = setup_database() # COMMENT OUT TO SAVE NEW DATA BETWEEN SESSIONS
    if successful:                # COMMENT OUT TO SAVE NEW DATA BETWEEN SESSIONS
        Interactive().cmdloop()
