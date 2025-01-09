import mysql.connector
import sys
import os

# Add the parent directory to the Python path

class DbModel:
    def __init__(self):
            self.db_name = 'db_managemen_uang_uas'
            self.connection = None
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database=self.db_name
                )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            if err.errno == 1049:  # Error: 1049 (42000): Unknown database
                print(f"Database {self.db_name} does not exist. Creating database...")
                self.connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password=''
                )
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"CREATE DATABASE {self.db_name}")
                self.connection.database = self.db_name
                print(f"Database {self.db_name} created successfully.")
                
                # insert schema
                if self.create_schema():
                    self.insert_data()
                else:
                    raise Exception("Error creating schema.")
    
    def close(self):
        try:
            if self.connection:
                self.connection.commit()
                self.connection.close()
            # print("Connection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")
            
    def check_connection(self):
        try:
            self.connect()
            print("Connected to database.")
            self.close()
            return True
        except Exception as e:
            print(e)
            return False
    
    def create_schema(self):
        try:
            self.connect()
            query = """
            CREATE TABLE IF NOT EXISTS savings (
                saving_id INT AUTO_INCREMENT PRIMARY KEY,
                saving_name VARCHAR(255) NOT NULL UNIQUE,
                balance DECIMAL(15, 2) NOT NULL DEFAULT 0
            );

            -- Table for Transaction Categories (e.g., Food, Home, Transport)
            CREATE TABLE IF NOT EXISTS transaction_categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(255) NOT NULL UNIQUE,
                category_type ENUM('expense','income') NOT NULL
            );

            -- Table for Transactions
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                saving_id INT, -- Source saving account
                destination_saving_id INT DEFAULT NULL, -- Destination saving account for transfers
                category_id INT DEFAULT NULL, -- For income/expense transactions
                transaction_type ENUM('income', 'expense', 'transfer') NOT NULL,
                transaction_date DATE NOT NULL,
                amount DECIMAL(15, 2) NOT NULL,
                notes TEXT,
                FOREIGN KEY (saving_id) REFERENCES savings(saving_id),
                FOREIGN KEY (destination_saving_id) REFERENCES savings(saving_id),
                FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id)
            );
            """
            self.cursor.execute(query, multi=True)
            print(f"Schema created successfully.")
            self.close()
            return True
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
        
    def insert_data(self):
        try:
            self.connect()
            query = """
            INSERT INTO transaction_categories (category_name, category_type) VALUES 
                ('Bills', 'expense'), 
                ('Transportation', 'expense'), 
                ('Home', 'expense'), 
                ('Electronics', 'expense'), 
                ('Education', 'expense'), 
                ('Entertainment', 'expense'), 
                ('Food', 'expense'), 
                ('Shopping', 'expense'), 
                ('Telephone', 'expense'), 
                ('Grants', 'income'), 
                ('Sale', 'income'), 
                ('Salary', 'income');
            """
            self.cursor.execute(query, multi=True)
            print("Data inserted successfully.")
            self.close()
        except Exception as e:
            print(f"Error inserting data: {e}")