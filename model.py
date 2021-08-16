#število vrstic in stolpcev
collumns = 7
rows = 6

#Za lepši zapis kasneje
EMPTY = " "
BGN = "Begin"

DRW = "Draw"
ERR = "Error"
HARD = "Hard"
EASY = "Easy"

PLYR = "Player"
CMPTR = "Computer"
PLYRS_1 = "Two_players_1"
PLYRS_2 = "Two_players_2"


class Game():
    board = [[EMPTY for _ in range(collumns)] for _ in range(rows)]
    
    def __init__(self, board, dificulty, player=PLYR):
        self.player = player
        self.dificulty = dificulty
        self.board = board
        if self.player == CMPTR:
                self.board[collumns - 1][(rows - 1) // 2] = CMPTR
                self.player = PLYR

    #preverjanje zmage
    def win(self):
        continue

    #izvajanje poteze igralca
    def move(self, collumn):
        continue