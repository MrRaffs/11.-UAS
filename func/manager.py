from common_imports import add_parent_dir
add_parent_dir()
from utils.dbcon import DbModel
from datetime import datetime


db = DbModel()

#debug
# db.check_connection()

#debug check import
# def check():
#     print("Ze blutof divaiz is Connected h succesfulley")


class ReportManager():
    # query untuk laporan
    def get_all_savings(self):
        db.connect()
        query = "SELECT * FROM savings"
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def get_income_category(self):
        db.connect()
        query = """
        SELECT * FROM transaction_categories
        WHERE category_type = 'income'
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def get_expense_category(self):
        db.connect()
        query = """
        SELECT * FROM transaction_categories
        WHERE category_type = 'expense'
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
        
    
    def get_transactions_by_month_year(self, month=None, year=None): # Query to get transactions by selected month and year
        db.connect()
        
        # If no month and year are provided, get the latest month and year in the database
        if not month or not year:
            latest_date_query = """
            SELECT DATE_FORMAT(MAX(transaction_date), '%Y-%m') AS latest_date
            FROM transactions;
            """
            db.cursor.execute(latest_date_query)
            latest_date = db.cursor.fetchone()
            if latest_date: #separate YYYY and MM
                latest_date = latest_date['latest_date'].split('-')
                year = latest_date[0]
                month = latest_date[1]
        
        if not month or not year:
            print("No data")
            db.close()
            return []
        
        query = """
        SELECT 
            t.transaction_id
            tc.category_name AS transaction_category_name,
            t.transaction_type,
            t.transaction_date,
            sc1.category_name AS source_category_name,
            sc2.category_name AS destination_category_name,
            t.amount,
            t.notes
        FROM 
            transactions t
        LEFT JOIN 
            savings s1 ON t.saving_id = s1.saving_id
        LEFT JOIN
            savings_categories sc1 ON s1.category_id = sc1.category_id
        LEFT JOIN 
            savings s2 ON t.destination_saving_id = s2.saving_id
        LEFT JOIN 
            savings_categories sc2 ON s2.category_id = sc2.category_id
        LEFT JOIN 
            transaction_categories tc ON t.category_id = tc.category_id
        WHERE 
            MONTH(t.transaction_date) = %s AND YEAR(t.transaction_date) = %s
        ORDER BY 
            t.transaction_date DESC;
        """
        db.cursor.execute(query, (month, year))
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    def expense_overview(self, month=None, year=None): # sort by the amount of expense of each category
        db.connect()
        
        # If no month and year are provided, get the latest month and year in the database
        if not month or not year:
            latest_date_query = """
            SELECT DATE_FORMAT(MAX(transaction_date), '%Y-%m') AS latest_date
            FROM transactions
            WHERE transaction_type = 'expense';
            """
            db.cursor.execute(latest_date_query)
            latest_date = db.cursor.fetchone()
            if latest_date:
                latest_date = latest_date['latest_date'].split('-')
                year = latest_date[0]
                month = latest_date[1]
        
        if not month or not year:
            print("No data")
            db.close()
            return []
        
        query = """
        SELECT
            t.transaction_id,
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
            t.transaction_type = 'expense' AND MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s
        GROUP BY sc.category_name, t.transaction_type, month
        ORDER BY total_expense DESC;
        """
        db.cursor.execute(query, (month, year))
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else print("No data")
        db.close()
        return result
    
    
class TransactionManager():
    def __init__(self, ):
        self.db = DbModel()
    
    # transaksi
    def add_income(self, account, amount, category, note, date=None):
        db.connect()
        if not date:
            date = datetime.now()
            
        query = """
        INSERT INTO transactions (saving_id, transaction_date, amount, category_id, notes, transaction_type)
        VALUES (%s, %s, %s, %s, %s, 'income');
        """
        db.cursor.execute(query, (account, date, amount, category, note))

        update_balance_query = """
        UPDATE savings
        SET balance = balance + %s
        WHERE saving_id = %s;
        """
        db.cursor.execute(update_balance_query, (amount, account))
        db.close()
    
    def add_expense(self, account, amount, category, note, date=None):
        db.connect()
        if not date:
            date = datetime.now()
            
        query = """
        INSERT INTO transactions (saving_id, transaction_date, amount, category_id, notes, transaction_type)
        VALUES (%s, %s, %s, %s, %s, 'expense');
        """
        db.cursor.execute(query, (account, date, amount, category, note))

        update_balance_query = """
        UPDATE savings
        SET balance = balance - %s
        WHERE saving_id = %s;
        """
        db.cursor.execute(update_balance_query, (amount, account))
        db.close()
    
    def add_transfer(self, account_source, account_destination, amount, category, note, date=None):
        db.connect()
        if not date:
            date = datetime.now()
            
        query = """
        INSERT INTO transactions (saving_id, destination_saving_id, transaction_date, amount, category_id, notes, transaction_type)
        VALUES (%s, %s, %s, %s, %s, %s, 'transfer');
        """
        db.cursor.execute(query, (account_source, account_destination, date, amount, category, note))

        update_source_balance_query = """
        UPDATE savings
        SET balance = balance - %s
        WHERE saving_id = %s;
        """
        db.cursor.execute(update_source_balance_query, (amount, account_source))

        update_destination_balance_query = """
        UPDATE savings
        SET balance = balance + %s
        WHERE saving_id = %s;
        """
        db.cursor.execute(update_destination_balance_query, (amount, account_destination))
        db.close()
        
        
    def edit_income(self, transaction_id, new_date=None, new_account=None, new_category=None, new_amount=None, new_note=None):
        db.connect()
        # Check if the transaction exists
        check_query = """
        SELECT COUNT(*) as count FROM transactions WHERE transaction_id = %s AND transaction_type = 'income';
        """
        db.cursor.execute(check_query, (transaction_id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No income transaction with this ID exists.")
            db.close()
            return
        
        update_fields = []
        update_values = []
        
        if new_date:
            update_fields.append("transaction_date = %s")
            update_values.append(new_date)
        if new_account:
            update_fields.append("saving_id = %s")
            update_values.append(new_account)
        if new_category:
            update_fields.append("category_id = %s")
            update_values.append(new_category)
        if new_amount:
            update_fields.append("amount = %s")
            update_values.append(new_amount)
        if new_note:
            update_fields.append("notes = %s")
            update_values.append(new_note)
        
        update_values.append(transaction_id)
        
        query = f"""
        UPDATE transactions
        SET {', '.join(update_fields)}
        WHERE transaction_id = %s;
        """
        db.cursor.execute(query, update_values)
        db.close()
    
    def edit_expense(self, transaction_id, new_date=None, new_account=None, new_category=None, new_amount=None, new_note=None):
        db.connect()
        # Check if the transaction exists
        check_query = """
        SELECT COUNT(*) as count FROM transactions WHERE transaction_id = %s AND transaction_type = 'expense';
        """
        db.cursor.execute(check_query, (transaction_id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No expense transaction with this ID exists.")
            db.close()
            return
        
        update_fields = []
        update_values = []
        
        if new_date:
            update_fields.append("transaction_date = %s")
            update_values.append(new_date)
        if new_account:
            update_fields.append("saving_id = %s")
            update_values.append(new_account)
        if new_category:
            update_fields.append("category_id = %s")
            update_values.append(new_category)
        if new_amount:
            update_fields.append("amount = %s")
            update_values.append(new_amount)
        if new_note:
            update_fields.append("notes = %s")
            update_values.append(new_note)
        
        update_values.append(transaction_id)
        
        query = f"""
        UPDATE transactions
        SET {', '.join(update_fields)}
        WHERE transaction_id = %s;
        """
        db.cursor.execute(query, update_values)
        db.close()
    
    def edit_transfer(self, transaction_id, new_date=None, new_account_src=None, new_account_dest=None, new_category=None, new_amount=None, new_note=None):
        db.connect()
        # Check if the transaction exists
        check_query = """
        SELECT COUNT(*) as count FROM transactions WHERE transaction_id = %s AND transaction_type = 'transfer';
        """
        db.cursor.execute(check_query, (transaction_id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No transfer transaction with this ID exists.")
            db.close()
            return
        
        update_fields = []
        update_values = []
        
        if new_date:
            update_fields.append("transaction_date = %s")
            update_values.append(new_date)
        if new_account_src:
            update_fields.append("saving_id = %s")
            update_values.append(new_account_src)
        if new_account_dest:
            update_fields.append("destination_saving_id = %s")
            update_values.append(new_account_dest)
        if new_category:
            update_fields.append("category_id = %s")
            update_values.append(new_category)
        if new_amount:
            update_fields.append("amount = %s")
            update_values.append(new_amount)
        if new_note:
            update_fields.append("notes = %s")
            update_values.append(new_note)
        
        update_values.append(transaction_id)
        
        query = f"""
        UPDATE transactions
        SET {', '.join(update_fields)}
        WHERE transaction_id = %s;
        """
        db.cursor.execute(query, update_values)
        db.close()
    
class CategoryManager():    
    # menambah kategori tabungan dan pengeluaran
    def add_savings(self, name, balance):
        db.connect()
        # Check if a savings account with the same name already exists
        check_query = """
        SELECT COUNT(*) as count FROM savings WHERE category_name = %s;
        """
        db.cursor.execute(check_query, (name,))
        count = db.cursor.fetchone()['count']
        
        if count > 0:
            print("A savings account with this name already exists.")
            db.close()
            return
        
        query = """
        INSERT INTO savings (category_name, balance)
        VALUES (%s, %s);
        """
        db.cursor.execute(query, (name, balance))
        db.close()
    
    def add_transaction_category(self, name, category_type):
        db.connect()
        # Check if a savings account with the same name already exists
        check_query = """
        SELECT COUNT(*) as count FROM transaction_categories WHERE category_name = %s;
        """
        db.cursor.execute(check_query, (name,))
        count = db.cursor.fetchone()['count']
        
        if count > 0:
            print("A savings account with this name already exists.")
            db.close()
            return
        
        query = """
        INSERT INTO transaction_categories (category_name, category_type)
        VALUES (%s, %s);
        """
        db.cursor.execute(query, (name, category_type))
        db.close()
    
    def delete_savings(self, id):
        db.connect()
        # Check if the savings account exists
        check_query = """
        SELECT COUNT(*) as count FROM savings WHERE saving_id = %s;
        """
        db.cursor.execute(check_query, (id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No savings account with this ID exists.")
            db.close()
            return
        
        query = """
        DELETE FROM savings WHERE saving_id = %s;
        """
        db.cursor.execute(query, (id,))
        db.close()
    
    def delete_transaction_category(self, id):
        db.connect()
        # Check if the transaction category exists
        check_query = """
        SELECT COUNT(*) as count FROM transaction_categories WHERE category_id = %s;
        """
        db.cursor.execute(check_query, (id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No transaction category with this ID exists.")
            db.close()
            return
        
        query = """
        DELETE FROM transaction_categories WHERE category_id = %s;
        """
        db.cursor.execute(query, (id,))
        db.close()

    def edit_savings(self, saving_id, new_balance, new_name=None):
        db.connect()
        # Check if the savings account exists
        check_query = """
        SELECT COUNT(*) as count FROM savings WHERE saving_id = %s;
        """
        db.cursor.execute(check_query, (saving_id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No savings account with this ID exists.")
            db.close()
            return
        
        if new_name:
            query = """
            UPDATE savings
            SET category_name = %s, balance = %s
            WHERE saving_id = %s;
            """
            db.cursor.execute(query, (new_name, new_balance, saving_id))
        else:
            query = """
            UPDATE savings
            SET balance = %s
            WHERE saving_id = %s;
            """
            db.cursor.execute(query, (new_balance, saving_id))
        
        db.close()
    
    def edit_transaction_category(self, tc_id, new_name=None, new_type=None):
        db.connect()
        # Check if the transaction category exists
        check_query = """
        SELECT COUNT(*) as count FROM transaction_categories WHERE category_id = %s;
        """
        db.cursor.execute(check_query, (tc_id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No transaction category with this ID exists.")
            db.close()
            return
        
        if new_name:
            query = """
            UPDATE transaction_categories
            SET category_name = %s
            WHERE category_id = %s;
            """
            db.cursor.execute(query, (new_name, tc_id))
        
        if new_type:
            query = """
            UPDATE transaction_categories
            SET category_type = %s
            WHERE category_id = %s;
            """
            db.cursor.execute(query, (new_type, tc_id))
        
        db.close()