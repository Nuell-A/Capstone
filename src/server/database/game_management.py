from .db_connection import Database
import random


class GameManagement:

    def __init__(self):
        self.db = Database()
        self.cursor = self.db.c.cursor()
        self.showAnswersTable()

    def showAnswersTable(self):
        print("Answers Table:")
        query = "SELECT * FROM answers"
        self.cursor.execute(query)

        print ("answer_id, question_id, answer_text")
        for row in self.cursor:
            print(row)
        print("")

    def close(self):
        self.cursor.close()
        self.db.closeConnection()

    def hostGame(self):
        game_id = self.uniqueGameID()
        print(game_id)

    def uniqueGameID(self):
        print("Creating Unique ID:")
        game_id = ""
        x = random.randint(100000, 999999)
        game_id = str(x)

        return game_id
    
gm = GameManagement()

gm.hostGame()