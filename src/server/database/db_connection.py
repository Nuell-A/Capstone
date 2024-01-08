import mysql.connector
import sys

sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")

import config



# Initiate connection
class Database:

    def __init__(self):
        # Database details
        self.config = {
        'user': config.user,
        'password': config.password,
        'host': config.host,
        'database': config.database,
        'raise_on_warnings': True,
        }

        self.c = None

        self.startConnection(self.config)
    
    def startConnection(self, config):
        try:
            self.c = mysql.connector.connect(**config)
            print("Connection successful.")
        except mysql.connector.Error as e:
            print(f"Error: {e}.")

    def closeConnection(self):
        try:
            self.c.close()
            print("Connection closed successfully.")
        except:
            print("There was an error when closing database connection.")

    def showAnswersTable(self, cursor):
        query = "SELECT * FROM answers"
        cursor.execute(query)

        for row in cursor:
            print(row)