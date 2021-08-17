#število vrstic in stolpcev
COLLUMNS = 7
ROWS = 6

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
    board = [[EMPTY for _ in range(COLLUMNS)] for _ in range(ROWS)]
    
    def __init__(self, board, dificulty, player=PLYR):
        self.player = player
        self.dificulty = dificulty
        self.board = board
        if self.player == CMPTR:        #če začne računalnik, da svoj prvi žeton na sredino (=> lahko predpostavimo da vedno začne igralec)
                self.board[COLLUMNS - 1][(ROWS - 1) // 2] = CMPTR
                self.player = PLYR


    #PREVERJANJE ZMAGE

    #iskanje štirih v vrsto
    def four_in_a_row(self, row, collumn):
        #iskati rabimo samo v te štiri smeri, ker bomo postore preverjali od spodaj navzgor in od leve proti desni
        directions = {(0, 1), (1, 1), (1, 0), (1, -1)} 
        starting_slot = self.board[row][collumn]
        if not starting_slot == EMPTY:
            for vec in directions:
                x, y = vec
                if 0 <= row + 3*y < ROWS and 0 <= collumn + 3*x < COLLUMNS:
                    if starting_slot == self.board[row + y][collumn + x] == self.board[row + 2*y][collumn + 2*x] == self.board[row + 3*y][collumn + 3*x]:
                        return starting_slot
        else:
            return EMPTY
        

    #preverjanje ali je igre konec => kdo je zmagovalec
    def win(self):
        is_draw = True
        #pregledamo vsa polja od spodaj navzgor (manj pregledovanja).
        #Ko najdemo polje ki je del štirih zaporednih, vrnemo zmagovalca. Če takega polja ni igro nadaljujemo ali zaključimo z remijem, če ni več prostih polj.
        for row in range(ROWS):
            for collumn in range(COLLUMNS):
                if self.board[row][collumn] == EMPTY:
                    draw_test = False
                elif self.four_in_a_row(row, collumn) == PLYR:
                    return PLYR
                elif self.four_in_a_row(row,collumn) == CMPTR:
                    return CMPTR
        if is_draw:
            return DRW
        else:
            return EMPTY #EMPTY AL ERR??? 
                





    #izvajanje poteze igralca
    def move(self, collumn):
        pass
        
    
