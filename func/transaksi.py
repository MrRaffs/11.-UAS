import mysql.connector

db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_managemen_uang_uas'
            )
cursor = db.cursor()

if db.is_connected():
    print("Connected to database")
    
cursor.execute("DROP TABLE `user`")