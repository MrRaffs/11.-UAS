from common_imports import add_parent_dir
add_parent_dir()

from func.manager import ReportManager, TransactionManager, CategoryManager 

class ReportUtils():
    def __init__(self):
        self.report = ReportManager()
    
    def show_all_balance(self):
        all_balance = ReportManager.get_all_savings()
        for savings in all_balance:
            print(f"{{saving id: {savings['id']}., saving_name: {savings['name']}, saving_balance: {savings['balance']}}}")
        
class TransactionUtils():
    pass
class CategoryUtils():
    pass