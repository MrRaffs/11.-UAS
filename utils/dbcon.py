import mysql.connector

class DbModel:
    def __init__(self):
            self.db_name = 'db_managemen_uang_uas'
            self.connection = None
            
    def check_connection(self):
        try:
            self.connect()
            self.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def check_if_exist(self, db_name):
        self.connect()
        self.cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = self.cursor.fetchone()
        if result:
            print(f"Database {db_name} exists.")
        else:
            print(f"Database {db_name} does not exist. Creating database...")
            self.cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully.")
            self.cursor.execute(schema)
            with open('schema.py', 'r') as schema_file:
                schema = schema_file.read()
            self.cursor.execute(schema)
        self.close()
        
    def connect(self):
        self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=self.db_name
            )
        self.cursor = self.connection.cursor()
    
