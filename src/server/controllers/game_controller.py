import sys

sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")

from server.database.game_management import GameManagement
from server.database.db_connection import Database


'''This class controls the flow of the game logic and is the median 
between the incoming requests from clients to ther server.'''

db = Database()
gm = GameManagement(db)
gm.showAnswersTable
questions = gm.getQuestions(1)
print(questions)