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
                self.execute_schema()
            else:
                raise
    
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
        
    def execute_schema(self):
        self.connect()
        # print(f"Database {self.db_name} created successfully.")
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as schema_file:
            schema = schema_file.read()
        self.cursor.execute(schema, multi=True)
        print("Tables created successfully.")
        with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'r') as data_file:
            data = data_file.read()
        self.cursor.execute(data, multi=True)
        print("Data inserted successfully.")
        self.close()
    