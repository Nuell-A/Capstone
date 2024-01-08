from db_connection import Database

db = Database()

cursor = db.c.cursor()

db.showAnswersTable(cursor)

cursor.close()

db.closeConnection()