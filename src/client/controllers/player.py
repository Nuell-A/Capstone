
class Player:
    '''Player object to hold player information'''

    def __init__(self):
        self.name = None
        self.score = 0
        self.game_id = None

    def getName(self):
        return self.name
    
    def setName(self, name: str):
        self.name = name

    def getScore(self):
        return self.score
    
    def setScore(self, score: int):
        self.score = score

    def getGameID(self):
        return self.game_id
    
    def setGameID(self, game_id):
        self.game_id = game_id
    
    def __str__(self):
        player_details = f"\nPlayer: {self.name}\nScore: {self.score}\nGame ID: {self.game_id}\n"
        return player_details