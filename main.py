from utils.dbcon import DbModel

db = DbModel()
db.check_connection()
db.check_if_exist()

