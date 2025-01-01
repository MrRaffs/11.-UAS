from helper import AppUtils
from dbcon import DbModel
from datetime import datetime
import os
import sys
app = AppUtils()
db = DbModel()


class Interface:
    def __init__(self):
        # Database initialization
        self.clear_screen()
        self.show_landing_page()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_landing_page(self):
        while True:
            self.clear_screen()
            print("=" * 50)
            print("MONEY MANAGEMENT SYSTEM")
            print("=" * 50)
            print("\n1. Start")
            print("2. Exit")
            
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == "1":
                self.show_main_menu()
            elif choice == "2":
                print("\nThank you for using Money Management System!")
                sys.exit()
            else:
                input("\nInvalid choice. Press Enter to continue...")
                
    def show_main_menu(self):
        while True:
            self.clear_screen()
            print("=" * 50)
            print("MAIN MENU")
            print("=" * 50)
            app.show_all_savings()
            print("=" * 50)
            print("\n1. Transaction")
            print("2. Report")
            print("3. Manage Savings and Categories")
            print("4. Back to Landing Page")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.show_transaction_menu()
            elif choice == "2":
                self.show_report_menu()
            elif choice == "3":
                self.show_manage_menu()
            elif choice == "4":
                self.show_landing_page()
            elif choice == "5":
                print("\nThank you for using Money Management System!")
                sys.exit()
            else:
                input("\nInvalid choice. Press Enter to continue...")
    
    def show_transaction_menu(self):
        while True:
            self.clear_screen()
            print("=" * 50)
            print("TRANSACTION MENU")
            print("=" * 50)
            print("\n1. Expense")
            print("2. Income")
            print("3. Transfer")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.add_transaction("expense")
            elif choice == "2":
                self.add_transaction("income")
            elif choice == "3":
                self.add_transaction("transfer")
            elif choice == "4":
                break
            else:
                input("\nInvalid choice. Press Enter to continue...")

    def add_transaction(self, trans_type):
        self.clear_screen()
        print(f"=" * 50)
        print(f"ADD {trans_type.upper()}")
        print(f"=" * 50)
        app.show_all_savings()
        print(f"=" * 50)
        
        # Get date
        while True:
            date_str = input("\nEnter date (YYYY-MM-DD) / press Enter to skip / input 0 to exit: ")
            if date_str == "":
                date_str = datetime.now().strftime('%Y-%m-%d')
                break
            elif date_str == "0":
                return
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")

        while True:
            try:
                account_choice = int(input("Select account number: "))
                if 1 <= account_choice <= app.get_max_saving_id():
                    account_id = account_choice 
                    break
                print("Invalid account number")
            except ValueError:
                print("Please enter a valid number")

        # Get amount
        while True:
            try:
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0")
                else: 
                    break
            except ValueError:
                print("Please enter a valid number")

        if trans_type == "transfer":
            while True:
                try:
                    dest_account_choice = int(input("Select destination account number: "))
                    if 1 <= dest_account_choice <= app.get_max_saving_id() and dest_account_choice != account_id:
                        dest_account_id = dest_account_choice
                        break
                    print("Invalid destination account number")
                except ValueError:
                    print("Please enter a valid number")
        else:
            # Get category 
            print("\nAvailable categories:")
            if trans_type == "income":
                app.show_income_transaction_category()
            elif trans_type == "expense":
                app.show_expense_transaction_category()
            min_category, max_category = app.get_transaction_category_minmax(trans_type)

            while True:
                try:
                    category_choice = int(input("\nSelect category number: "))
                    if min_category <= category_choice <= max_category:
                        category = category_choice
                        break
                    print("Invalid category number")
                except ValueError:
                    print("Please enter a valid number")

        # Get note
        note = input("\nEnter note (optional): ")

        # Confirm transaction
        print("\nTransaction Details:")
        print(f"Date: {date_str}")
        print(f"Type: {trans_type}")
        app.show_savings_by_id(account_id)
        print(f"Amount: Rp {amount:,.2f}")
        if trans_type == "transfer":
            print("Dest ", end="")
            app.show_savings_by_id(dest_account_id)
            # app.show_savings_by_id(dest_account_id)
        else:
            app.show_transaction_category_by_id(category)
        print(f"Note: {note}")

        confirm = input("\nConfirm transaction? (y/n): ").lower()
        if confirm == 'y':
            # Add transaction to the database
            if trans_type == "transfer":
                app.add_transfer(account_id, dest_account_id, amount, note, date_str)
            elif trans_type == "income":
                app.add_income(account_id, amount, category, note, date_str)
            elif trans_type == "expense":
                app.add_expense(account_id, amount, category, note, date_str)
            print("\nTransaction added successfully.")
        else:
            print("\nTransaction cancelled.")

        input("\nPress Enter to continue...")

    def show_report_menu(self):
        while True:
            self.clear_screen()
            print("=" * 50)
            print("REPORT MENU")
            print("=" * 50)
            print("\n1. View Transactions")
            print("2. Expense Overview")
            print("3. Back to Main Menu")

            choice = input("\nEnter your choice (1-3): ")

            if choice == "1":
                self.view_transactions()
            elif choice == "2":
                self.view_expense_overview()
            elif choice == "3":
                break
            else:
                input("\nInvalid choice. Press Enter to continue...")

    def view_transactions(self):
        self.clear_screen()
        print("=" * 50)
        print("TRANSACTION REPORT")
        print("=" * 50)
        
        while True:
            date_str = input("\nEnter date (YYYY-MM) / press Enter to skip / input 0 to exit: ")
            if date_str == "":
                date_str = datetime.now().strftime('%Y-%m')
                break
            elif date_str == "0":
                return
            try:
                datetime.strptime(date_str, '%Y-%m')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM")

        year = int(date_str.split("-")[0])
        month = int(date_str.split("-")[1])
        
        app.show_all_transactions(year,month)
        print("=" * 50)
        app.show_summary(year,month)
        print("=" * 50)
        while True:
            choice = input("\nEnter : 0 back/ 1 edit / 2 delete: ")
            if choice == "0":
                return
            elif choice == "1":
                self.edit_transaction()
            elif choice == "2":
                self.delete_transaction()
            else:
                input("\nInvalid choice. Press Enter to continue...")
    
    def view_expense_overview(self):
        self.clear_screen()
        print("=" * 50)
        print("EXPENSE OVERVIEW")
        print("=" * 50)
        
        while True:
            date_str = input("\nEnter date (YYYY-MM) / press Enter to skip / input 0 to exit: ")
            if date_str == "":
                date_str = datetime.now().strftime('%Y-%m')
                break
            elif date_str == "0":
                return
            try:
                datetime.strptime(date_str, '%Y-%m')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM")

        year = int(date_str.split("-")[0])
        month = int(date_str.split("-")[1])
        
        app.show_expense_overview(year, month)
        input("\nPress Enter to continue...")
            
ui = Interface()
ui.show_main_menu()