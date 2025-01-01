from common_imports import add_parent_dir
add_parent_dir()

from func.manager import ReportManager, TransactionManager, CategoryManager 

class ReportUtils():
    def __init__(self):
        self.report = ReportManager()

    def show_all_balance(self):
        all_balance = self.report.get_all_savings()
        for savings in all_balance:
            print(f"{savings['saving_id']}. || Account: {savings['saving_name']} \t|| Balance: {savings['saving_balance']}")
    
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
            
test = ReportUtils()
# test.show_all_transactions(2024, 11)
# test.show_expense_overview(2024,10)
# test.show_expense_transaction_category()
# test.show_income_transaction_category()

class TransactionUtils():
    pass
class CategoryUtils():
    pass