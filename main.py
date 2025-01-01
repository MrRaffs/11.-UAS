from utils.dbcon import DbModel
from utils.ui import Interface
from utils.common_imports import *
from time import sleep

def init():
    db = DbModel()
    if db.check_connection():
        db.check_if_exist()
        sleep(0.5)
        input("Press Enter to continue...")
        
    else:
        print("Error connecting to database.")
        sys.exit(1)
    Interface()
if __name__ == "__main__":
    init()
