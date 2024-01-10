import mysql.connector
import sys

sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")

import config



# Initiate connection
class Database:
    '''This class handles the connection to the database.'''

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

        self.startConnection()
    
    def startConnection(self):
        print("Connecting to database...")
        try:
            with mysql.connector.connect(**self.config) as conn:
                self.c = conn
                
            print("Connection successful.\n")
        except mysql.connector.Error as e:
            print(f"Error: {e}.\n")

    def closeConnection(self):
        print("Closing database...")
        try:
            self.c.close()
            print("Connection closed successfully.\n")
        except:
            print("There was an error when closing database connection.\n")

