from common_imports import add_parent_dir
add_parent_dir()

from func.manager import ReportManager, TransactionManager, CategoryManager 

class AppUtils():
    def __init__(self):
        self.report = ReportManager()
        self.transaction = TransactionManager()
        self.category = CategoryManager()

    def show_all_savings(self):
        all_balance = self.report.get_all_savings()
        for savings in all_balance:
            print(f"{savings['saving_id']}. || Account: {savings['saving_name']} \t|| Balance: {savings['saving_balance']}")
    
    def show_savings_by_id(self, saving_id):
        saving = self.report.get_savings_by_id(saving_id)
        print(f"Account: {saving['saving_name']} || Balance: {saving['saving_balance']}")
        return saving
        
    def show_all_transactions(self, month=None, year=None):
        all_transactions = self.report.get_transactions_by_month_year(month, year)
        if all_transactions is None:
            print("No transactions found for the given month and year.")
            return
        for transaction in all_transactions:
            if transaction['transaction_type'] == 'expense' or transaction['transaction_type'] == 'income':
                print(f"ID :{transaction['transaction_id']}\n    Type: {transaction['transaction_type']}\n    {transaction['transaction_category_name']}\n    Date: {transaction['transaction_date']}\n    Source: {transaction['source_category_name']}\n    Amount: Rp.{transaction['amount']}\n    Notes: {transaction['notes']}\n-------------------------")
            else:
                print(f"ID :{transaction['transaction_id']}\n    Type: {transaction['transaction_type']}\n    Date: {transaction['transaction_date']}\n    Source: {transaction['source_category_name']}\n    Destination: {transaction['destination_category_name']}\n    Amount: Rp.{transaction['amount']}\n    Notes: {transaction['notes']}\n-------------------------")

    def show_transaction_by_id(self, transaction_id):
        transaction = self.report.get_transaction_by_id(transaction_id)
        if transaction['transaction_type'] == 'expense' or transaction['transaction_type'] == 'income':
                print(f"ID :{transaction['transaction_id']}\n    Type: {transaction['transaction_type']}\n    {transaction['transaction_category_name']}\n    Date: {transaction['transaction_date']}\n    Source: {transaction['source_category_name']}\n    Amount: Rp.{transaction['amount']}\n    Notes: {transaction['notes']}\n-------------------------")
        else:
            print(f"ID :{transaction['transaction_id']}\n    Type: {transaction['transaction_type']}\n    Date: {transaction['transaction_date']}\n    Source: {transaction['source_category_name']}\n    Destination: {transaction['destination_category_name']}\n    Amount: Rp.{transaction['amount']}\n    Notes: {transaction['notes']}\n-------------------------")
    
    def show_expense_overview(self, year=None, month=None):
        expense_overview = self.report.expense_overview(year, month)
        if expense_overview is None:
            print("No transactions found for the given month and year.")
            return
        print(f"Total expense in {expense_overview[0]['month']}\n------------------------------------------------")
        for expense in expense_overview:
            print(f"{expense['category_name']}\nRp.{expense['total_expense']}\n")

    def show_income_transaction_category(self):
        income_tc = self.report.get_income_transaction_category()
        for category in income_tc:
            print(f"{category['category_id']}. {category['category_name']}")
            
    def show_expense_transaction_category(self):
        expense_tc = self.report.get_expense_transaction_category()
        for category in expense_tc:
            print(f"{category['category_id']}. {category['category_name']}")
    
    #Transaction manager
    def add_income(self, account, amount, category, note, date=None):
        try:
            saving = self.report.get_savings_by_id(account)
                    
            self.transaction.add_income(account, amount, category, note, date)   
            print(f"Income Rp.{amount} added to {saving['saving_name']} successfully.")
            
            print("-------------------------\nBALANCES AFTER\n")
            AppUtils.show_all_savings(self)
        except Exception as e:
            print(f"\nError adding income: {e}\n")
    
    
    # REPORT MANAGER
    def add_expense(self, account, amount, category, note, date=None):
        try:
            saving = self.report.get_savings_by_id(account)
                 
            self.transaction.add_expense(account, amount, category, note, date)   
            print(f"Expense Rp.{amount} deducted from {saving['saving_name']} successfully.")
            
            print("-------------------------\nBALANCES AFTER\n")
            AppUtils.show_all_savings(self)
        except Exception as e:
            print(f"\nError adding expense: {e}\n")
            
    def add_transfer(self, source_account, destination_account, amount, note, date=None):
        try:
            source_saving = self.report.get_savings_by_id(source_account)
            destination_saving = self.report.get_savings_by_id(destination_account)

            self.transaction.add_transfer(source_account, destination_account, amount, note, None, date)
            print(f"Transfer Rp.{amount} from {source_saving['saving_name']} to {destination_saving['saving_name']} successfully.")

            print("-------------------------\nBALANCES AFTER\n")
            AppUtils.show_all_savings(self)
        except Exception as e:
            print(f"\nError adding transfer: {e}\n")
    
    def edit_transaction(self, transaction_id, new_amount, new_category=None, new_note=None, new_date=None):
        
        pass
    
    def delete_transaction(self, transaction_id):
        pass
    
    # CATEGORY MANAGER
    def add_saving(self, saving_name, saving_balance):
        try:
            self.category.add_saving(saving_name, saving_balance)
            print(f"Account {saving_name} added successfully.")
        except Exception as e:
            print(f"\nError adding account: {e}\n")
    
    def delete_saving(self, saving_id):
        try:
            saving = self.report.get_savings_by_id(saving_id)
            self.category.delete_savings(saving_id)
            print(f"Account {saving['saving_name']} deleted successfully.")
        except Exception as e:
            print(f"\nError deleting account: {e}\n")
            
    def edit_saving(self, saving_id, new_balance, new_name=None):
        try:
            saving = self.report.get_savings_by_id(saving_id)
            self.category.edit_savings(saving_id, new_balance, new_name)
            print(f"Account {saving['saving_name']} edited successfully.")
        except Exception as e:
            print(f"\nError editing account: {e}\n")
            
    def add_transaction_category():
        pass
    
    def edit_transaction_category():
        pass
    
    def delete_transaction_category():
        pass
    
            
test = AppUtils()
# test.show_all_transactions(2024, 11)
# test.show_expense_overview(2024,10)
# test.show_expense_transaction_category()
# test.show_income_transaction_category()

# test.add_income(1, 1000000, 1, 'test income')
# test.add_expense(1, 1000000, 1, 'test expense')
# test.add_transfer(1, 2, 1000000, 'test transfer')
# test.show_transaction_by_id(21)

# test.add_saving('test', 1000000)
# test.delete_saving(3)


test.show_all_savings()
