import copy
import random
import json

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
            return EMPTY            


    #POTEZE

    #pomožne metode za izvajanje poteze
    @staticmethod
    def move_is_possible(board, collumn):
        return board[0][collumn] == EMPTY

    #poišče prvo prazno mesto v stolpcu, ki ga je izbral igralec
    @staticmethod
    def collumn_move(player, board, collumn):
        for row in range(ROWS - 1, -1, -1):
            if board[row][collumn] == EMPTY:
                board[row][collumn] == player
                return board


    #POTEZA RAČUNALNIKA

    #poišče vse poteze, s katerimi lahko računalnik ali igralec (s svojo naslednjo potezo) zaključita igro
    def game_ending_moves(self):
        game_enders = set()
        current_game_board = copy.deepcopy(self.board)
        for collumn in range(COLLUMNS):
            board = copy.deepcopy(current_game_board)
            if Game.move_is_possible(board, collumn):
                self.board = Game.collumn_move(CMPTR, board, collumn)
                if self.win() == CMPTR:
                    game_enders.add((CMPTR, collumn))
                board = copy.deepcopy(current_game_board)
                self.board = Game.collumn_move(PLYR, board, collumn)
                if self.win() == PLYR:
                    game_enders.add((PLYR, collumn))
        self.board = copy.deepcopy(current_game_board)
        return game_enders

    

    #POTEZA IGRALCA

    #Poteza igralca v igri proti računalniku
    def single_player_move(self, collumn):
        board = copy.deepcopy(self.board)
        if not Game.move_is_possible(board, collumn):
            return ERR
        else:
            self.board = Game.collumn_move(PLYR, self.board, collumn)
            outcome = self.win()
            if outcome == PLYR or outcome == CMPTR:
                return outcome
            else:
                self.computer_move()
                return self.win()
    
    #Poteza igralca v igri med dvema igralcema
    def two_player_move(self, collumn):
        if self.player == PLYRS_1:
            board = copy.deepcopy(self.board)
            if not Game.move_is_possible(board, collumn):
                return ERR
            else:
                self.board = Game.collumn_move(PLYR, self.board, collumn)
                outcome = self.win()
                self.player = PLYRS_2
                return outcome
        elif self.player == PLYRS_2:
            board = copy.deepcopy(self.board)
            if not Game.move_is_possible(board, collumn):
                return ERR
            else:
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                outcome = self.win()
                self.player = PLYRS_1
                return outcome
        else:
            assert False


    #funkcija, ki jo kličemo vedno, ko je na potezi igralec
    def player_move(self, collumn):
        if self.player == PLYRS_1 or self.player == PLYRS_2:
            return self.two_player_move(collumn)
        else:
            return self.single_player_move(collumn)
        


class ActiveGame():
    def __init__(self, current_board_file):
        self.current_board_file = current_board_file
        self.games = {}

    def game_id_open(self):
        if self.games == {}:
            return 0
        else:
            for i in range(len(self.games) + 1):
                if i not in self.games.keys():
                    return i
    
    def new_game(self, player=PLYR, dificulty=HARD):
        pass
