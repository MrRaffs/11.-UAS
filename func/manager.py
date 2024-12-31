from common_imports import add_parent_dir
add_parent_dir()
from utils.dbcon import DbModel

db = DbModel()

#debug
# db.check_connection()

#debug check import
# def check():
#     print("Ze blutof divaiz is Connected h succesfulley")


class ReportManager():
    # query untuk laporan
    def get_all_balance(self):
        db.connect()
        query = "SELECT * FROM savings"
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def get_all_transactions(self): #Query mengabil semua data transaksi paling akhir
        db.connect()
        query = """
        SELECT 
	        sc1.category_name AS source_category_name,
	        sc2.category_name AS destination_category_name,
	        tc.category_name AS transaction_category_name,
	        t.transaction_type,
	        t.transaction_date,
	        t.amount,
	        t.notes
        FROM 
            	transactions t
            -- Join to get source saving account details
            LEFT JOIN 
            	savings s1 ON t.saving_id = s1.saving_id
            LEFT JOIN
            	savings_categories sc1 ON s1.category_id = sc1.category_id
            -- Join to get destination saving account details
            LEFT JOIN 
            	savings s2 ON t.destination_saving_id = s2.saving_id
            LEFT JOIN 
            	savings_categories sc2 ON s2.category_id = sc2.category_id
            -- Join to get transaction category details
            LEFT JOIN 
            	transaction_categories tc ON t.category_id = tc.category_id;
        ORDER BY t.transaction_date DESC;
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def get_income(self):
        db.connect()
        query = """
        SELECT
            sc.category_name AS source_category_name,
            t.transaction_type,
            t.transaction_date,
            t.amount,
            t.notes
        FROM
            transactions t
        LEFT JOIN
            savings s ON t.saving_id = s.saving_id
        LEFT JOIN
            savings_categories sc ON s.category_id = sc.category_id
        WHERE
            t.transaction_type = 'income'
        ORDER BY t.transaction_date DESC;
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def get_expense(self):
        db.connect()
        query = """
        SELECT
            sc.category_name AS source_category_name,
            t.transaction_type,
            t.transaction_date,
            t.amount,
            t.notes
        FROM
            transactions t
        LEFT JOIN
            savings s ON t.saving_id = s.saving_id
        LEFT JOIN
            savings_categories sc ON s.category_id = sc.category_id
        WHERE
            t.transaction_type = 'expense'
        ORDER BY t.transaction_date DESC;
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def get_transfer(self):
        db.connect()
        query = """
        SELECT
            sc.category_name AS source_category_name,
            sd.category_name AS destination_category_name,
            t.transaction_type,
            t.transaction_date,
            t.amount,
            t.notes
        FROM
            transactions t
        LEFT JOIN
            savings s1 ON t.saving_id = s1.saving_id
        LEFT JOIN
            savings s2 ON t.destination_saving_id = s2.saving_id
        LEFT JOIN
            savings_categories sc ON s.category_id = sc.category_id
        LEFT JOIN
            savings_categories sd ON s.category_id = sd.category_id
        WHERE
            t.transaction_type = 'expense'
        ORDER BY t.transaction_date DESC;
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def expense_overview(self): # sort by the amount of expense of each category
        db.connect()
        query = """
         SELECT
            sc.category_name AS source_category_name,
            t.transaction_type,
            DATE_FORMAT(transaction_date, '%Y-%m') AS month,
            SUM(t.amount) AS total_expense
        FROM
            transactions t
        LEFT JOIN
            savings s ON t.saving_id = s.saving_id
        LEFT JOIN
            savings_categories sc ON s.category_id = sc.category_id
        WHERE
            t.transaction_type = 'expense' 
        GROUP BY sc.category_name, t.transaction_type, transaction_month
        ORDER BY total_expense DESC;
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
        pass
    
    
class TransactionManager():
    def __init__(self, ):
        self.db = DbModel()
    
    # transaksi
    def add_income(self, amount, note):
        pass
    
    def add_expense(self, amount, note):
        pass
    
    def add_transfer(self, amount, destination, note):
        pass
    
    def edit_income(self, transaction_id, amount, note=None):
        pass
    
    def edit_expense(self, transaction_id, amount, note=None):
        pass
    
    def edit_transfer(self, transaction_id, amount, destination, note=None):
        pass
    
class CategoryManager():    
    # menambah kategori tabungan dan pengeluaran
    def add_savings(self):
        pass
    
    def add_expense_category(self):
        pass