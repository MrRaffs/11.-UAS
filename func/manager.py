from .common_imports import add_parent_dir
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
    def __init__(self):
        self.db = DbModel()
    # query untuk laporan
    def get_all_savings(self):
        db.connect()
        query = """
        SELECT saving_id, saving_name, balance AS saving_balance 
        FROM savings;
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else None
        db.close()
        return result
    def get_max_saving_id(self):
        db.connect()
        query = """
        SELECT MAX(saving_id) AS max_saving_id FROM savings;
        """
        db.cursor.execute(query)
        row = db.cursor.fetchone()
        result = row['max_saving_id'] if row else None
        db.close()
        return result
    
    def get_savings_by_id(self, saving_id):
        db.connect()
        query = """
        SELECT saving_id, saving_name, balance AS saving_balance 
        FROM savings
        WHERE saving_id = %s;
        """
        db.cursor.execute(query, (saving_id,))
        row = db.cursor.fetchone()
        result = dict(row) if row else None
        db.close()
        return result
    
    def get_income_transaction_category(self):
        db.connect()
        query = """
        SELECT * FROM transaction_categories
        WHERE category_type = 'income'
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else None
        db.close()
        return result
    
    def get_expense_transaction_category(self):
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
    def get_transaction_category_by_id(self, category_id):
        db.connect()
        query = """
        SELECT * FROM transaction_categories
        WHERE category_id = %s
        """
        db.cursor.execute(query, (category_id,))
        row = db.cursor.fetchone()
        result = dict(row) if row else None
        db.close()
        return result
    
    def get_transaction_category_minmax(self, category_type):
        db.connect()
        query = """
        SELECT MIN(category_id) AS min_category_id, MAX(category_id) AS max_category_id 
        FROM transaction_categories
        WHERE category_type = %s
        """
        db.cursor.execute(query, (category_type,))
        row = db.cursor.fetchone()
        min_category_id = row['min_category_id'] if row else None
        max_category_id = row['max_category_id'] if row else None
        db.close()
        return min_category_id, max_category_id
    
    def get_transactions_by_month_year(self, year=None, month=None): # Query to get transactions by selected month and year
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
            t.transaction_id,
            tc.category_name AS transaction_category_name,
            t.transaction_type,
            t.transaction_date,
            s1.saving_name AS source_category_name,
            s2.saving_name AS destination_category_name,
            t.amount,
            t.notes
        FROM 
            transactions t
        LEFT JOIN 
            savings s1 ON t.saving_id = s1.saving_id
        LEFT JOIN 
            savings s2 ON t.destination_saving_id = s2.saving_id
        LEFT JOIN 
            transaction_categories tc ON t.category_id = tc.category_id
        WHERE 
            MONTH(t.transaction_date) = %s AND YEAR(t.transaction_date) = %s
        ORDER BY 
            t.transaction_date ASC;
        """
        db.cursor.execute(query, (month, year))
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else None
        db.close()
        return result
    
    def get_transaction_by_id(self, transaction_id):
        db.connect()
        query = """
        SELECT 
            t.transaction_id,
            tc.category_name AS transaction_category_name,
            t.transaction_type,
            t.transaction_date,
            s1.saving_name AS source_category_name,
            s2.saving_name AS destination_category_name,
            t.amount,
            t.notes
        FROM 
            transactions t
        LEFT JOIN 
            savings s1 ON t.saving_id = s1.saving_id
        LEFT JOIN 
            savings s2 ON t.destination_saving_id = s2.saving_id
        LEFT JOIN 
            transaction_categories tc ON t.category_id = tc.category_id
        WHERE 
            t.transaction_id = %s;
        """
        db.cursor.execute(query, (transaction_id,))
        row = db.cursor.fetchone()
        result = dict(row) if row else None
        db.close()
        return result
    
    def expense_overview(self, year=None, month=None): # sort by the amount of expense of each category
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
            tc.category_name AS category_name,
            DATE_FORMAT(transaction_date, '%Y-%m') AS month,
            SUM(t.amount) AS total_expense
        FROM
            transactions t
        LEFT JOIN
            transaction_categories tc ON t.category_id = tc.category_id
        WHERE
            t.transaction_type = 'expense' AND MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s
        GROUP BY tc.category_name
        ORDER BY total_expense DESC;
        """
        db.cursor.execute(query, (month, year))
        rows = db.cursor.fetchall()
        result = [dict(row) for row in rows] if rows else None
        db.close()
        return result
    
    def get_summary(self, year=None, month=None):
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
            
        income_query = """
        SELECT SUM(amount) AS total_income
        FROM transactions
        WHERE transaction_type = 'income' AND MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s;
        """
        expense_query = """
        SELECT SUM(amount) AS total_expense
        FROM transactions
        WHERE transaction_type = 'expense' AND MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s;
        """

        db.cursor.execute(income_query, (month, year))
        total_income = db.cursor.fetchone()['total_income'] or 0

        db.cursor.execute(expense_query, (month, year))
        total_expense = db.cursor.fetchone()['total_expense'] or 0

        net_change = total_income - total_expense

        db.close()

        return {
            'date': f"{year}-{month}",
            'total_income': total_income,
            'total_expense': total_expense,
            'net_change': net_change
        }
    
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
    
    def add_transfer(self, account_source, account_destination, amount, note, category=None, date=None):
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
        
        
    def edit_transaction(self, transaction_id, new_date=None, new_account=None, new_account_dest=None, new_category=None, new_amount=None, new_note=None):
        db.connect()
        # Check if the transaction exists
        check_query = """
        SELECT transaction_type, saving_id, destination_saving_id, amount FROM transactions WHERE transaction_id = %s;
        """
        db.cursor.execute(check_query, (transaction_id,))
        transaction = db.cursor.fetchone()
        
        if not transaction:
            print("No transaction with this ID exists.")
            db.close()
            return
        
        transaction_type = transaction['transaction_type']
        old_saving_id = transaction['saving_id']
        old_dest_saving_id = transaction['destination_saving_id']
        old_amount = transaction['amount']
        
        update_fields = []
        update_values = []
        
        if new_date:
            update_fields.append("transaction_date = %s")
            update_values.append(new_date)
        else:
            new_date = datetime.now()
            update_fields.append("transaction_date = %s")
            update_values.append(new_date)
            
        if new_account and new_account != old_saving_id:
            update_fields.append("saving_id = %s")
            update_values.append(new_account)
            
        if new_account_dest and transaction_type == 'transfer' and new_account_dest != old_dest_saving_id:
            update_fields.append("destination_saving_id = %s")
            update_values.append(new_account_dest)
        if new_category:
            update_fields.append("category_id = %s")
            update_values.append(new_category)
        if new_amount is not None and new_amount != old_amount:
            amount_difference = new_amount - old_amount
            
            if transaction_type == 'income':
                balance_update_query = """
                UPDATE savings
                SET balance = balance + %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(balance_update_query, (amount_difference, old_saving_id))
            elif transaction_type == 'expense':
                balance_update_query = """
                UPDATE savings
                SET balance = balance - %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(balance_update_query, (amount_difference, old_saving_id))
            elif transaction_type == 'transfer':
                # Revert old balances
                source_balance_update_query = """
                UPDATE savings
                SET balance = balance + %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(source_balance_update_query, (old_amount, old_saving_id))
                
                destination_balance_update_query = """
                UPDATE savings
                SET balance = balance - %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(destination_balance_update_query, (old_amount, old_dest_saving_id))
                
                # Apply new balances
                new_source_balance_update_query = """
                UPDATE savings
                SET balance = balance - %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(new_source_balance_update_query, (new_amount, new_account))
                
                new_destination_balance_update_query = """
                UPDATE savings
                SET balance = balance + %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(new_destination_balance_update_query, (new_amount, new_account_dest))
            
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
    
    def delete_transaction(self, transaction_id):
        db.connect()
        # Check if the transaction exists
        check_query = """
        SELECT COUNT(*) as count FROM transactions WHERE transaction_id = %s;
        """
        db.cursor.execute(check_query, (transaction_id,))
        count = db.cursor.fetchone()['count']
        
        if count == 0:
            print("No transaction with this ID exists.")
            db.close()
            return
        
        # Get transaction details to update the balance
        transaction_query = """
        SELECT saving_id, destination_saving_id, amount, transaction_type
        FROM transactions
        WHERE transaction_id = %s;
        """
        db.cursor.execute(transaction_query, (transaction_id,))
        transaction = db.cursor.fetchone()
        
        if transaction:
            saving_id = transaction['saving_id']
            destination_saving_id = transaction['destination_saving_id']
            amount = transaction['amount']
            transaction_type = transaction['transaction_type']
            
            if transaction_type == 'income':
                update_balance_query = """
                UPDATE savings
                SET balance = balance - %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(update_balance_query, (amount, saving_id))
            
            elif transaction_type == 'expense':
                update_balance_query = """
                UPDATE savings
                SET balance = balance + %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(update_balance_query, (amount, saving_id))
            
            elif transaction_type == 'transfer':
                update_source_balance_query = """
                UPDATE savings
                SET balance = balance + %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(update_source_balance_query, (amount, saving_id))
                
                update_destination_balance_query = """
                UPDATE savings
                SET balance = balance - %s
                WHERE saving_id = %s;
                """
                db.cursor.execute(update_destination_balance_query, (amount, destination_saving_id))
        
        # Delete the transaction
        delete_query = """
        DELETE FROM transactions WHERE transaction_id = %s;
        """
        db.cursor.execute(delete_query, (transaction_id,))
        db.close()
class CategoryManager():    
    # menambah kategori tabungan dan pengeluaran
    def add_saving(self, name, balance):
        db.connect()
        # Check if a savings account with the same name already exists
        check_query = """
        SELECT COUNT(*) as count FROM savings WHERE saving_name = %s;
        """
        db.cursor.execute(check_query, (name,))
        count = db.cursor.fetchone()['count']
        
        if count > 0:
            print("A savings account with this name already exists.")
            db.close()
            return
        
        query_saving = """
        INSERT INTO savings (saving_name, balance)
        VALUES (%s, %s);
        """
        db.cursor.execute(query_saving, (name, balance))
        db.close()
    
    def add_transaction_category(self, name, category_type):
        db.connect()
        # Check if a transaction category with the same name already exists
        check_query = """
        SELECT COUNT(*) as count FROM transaction_categories WHERE category_name = %s;
        """
        db.cursor.execute(check_query, (name,))
        count = db.cursor.fetchone()['count']
        
        if count > 0:
            print("A transaction category with this name already exists.")
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
        
        if new_name and new_balance:
            query = """
            UPDATE savings
            SET saving_name = %s, balance = %s
            WHERE saving_id = %s;
            """
            db.cursor.execute(query, (new_name, new_balance, saving_id))
        if new_name:
            query = """
            UPDATE savings
            SET saving_name = %s
            WHERE saving_id = %s;
            """
            db.cursor.execute(query, (new_name, saving_id))
        if new_balance:
            query = """
            UPDATE savings
            SET balance = %s
            WHERE saving_id = %s;
            """
            db.cursor.execute(query, (new_balance, saving_id))
        else:
            print("No changes made.")
        
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
