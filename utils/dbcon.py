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
        self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=self.db_name
            )
        self.cursor = self.connection.cursor(dictionary=True)
    
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
        
    def check_if_exist(self):
        self.connect()
        self.cursor.execute(f"SHOW DATABASES LIKE '{self.db_name}'")
        result = self.cursor.fetchone()
        if result:
            print(f"Database {self.db_name} exists.")
        else:
            print(f"Database {self.db_name} does not exist. Creating database...")
            self.cursor.execute(f"CREATE DATABASE {self.db_name}")
            print(f"Database {self.db_name} created successfully.")
            self.cursor.execute(schema)
            with open('schema.py', 'r') as schema_file:
                schema = schema_file.read()
            self.cursor.execute(schema)
        self.close()
    