import random


class GameManagement:
    '''This class will hold all of the game logic needed for the database.'''

    def __init__(self, db):
        self.db = db

    def showAnswersTable(self):
        '''Gets data from answers table'''

        cursor = self.db.c.cursor()

        print("Answers Table:")
        query = "SELECT * FROM answers"

        cursor.execute(query)

        print ("answer_id, question_id, answer_text")
        for row in self.cursor:
            print(row)
        print("")

    def close(self):
        self.db.closeConnection()

    def hostGame(self):
        '''Creates unique game id, and inserts new row into quiz_sessions table.'''

        print("Starting hostint process...")
        try:
            cursor = self.db.c.cursor()
            game_id = self.uniqueGameID()
            host_user = 'test'
            is_active = 1 # is_active: 1 for true, 0 for false.

            query = "INSERT INTO quiz_sessions(game_id, host_user, is_active) VALUES(%s, %s, %s)"
            cursor.execute(query, (game_id, host_user, is_active))

            print(game_id)
            print("Game successfully hosted, please share the Game ID with other players.")
        except:
            print("There was an error hosting your game.")

    def uniqueGameID(self):
        '''Creates unique ID with random module.'''

        print("Creating Unique ID:")
        game_id = ""
        x = random.randint(100000, 999999)
        game_id = str(x)

        return game_id
    
    def getQuestions(self, size: int):
        '''Creates question set from database. 'size' is the number of questions for the question set.
        QuestionsTable: question_id, game_id, question_text, correct_answer'''

        questions = []
        cursor = self.db.c.cursor()

        print("Getting questions set:")

        query = "SELECT * FROM questions ORDER BY RAND() LIMIT %s"
        cursor.execute(query, (size,))
        '''fetchall() returns a list of tuples where each tuple is a row.
          e.g. [(row1), (row2), etc.]'''
        questions = cursor.fetchall() # Gets all values from 

        print("Questions set created")
        return questions