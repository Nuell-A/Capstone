
class Player:
    '''Player object to hold player information'''

    def __init__(self):
        self.name = None
        self.score = 0

    def getName(self):
        return self.name
    
    def setName(self, name: str):
        self.name = name

    def getScore(self, score: int):
        self.score = score

    def __str__(self):
        player_details = f"Player: {self.name}\nScore: {self.score}\n"
        return player_details