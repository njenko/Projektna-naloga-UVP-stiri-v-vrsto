import copy
import random
import json

#število vrstic in stolpcev
COLLUMNS = 7
ROWS = 6

#Za lepši zapis kasneje
EMPTY = "Empty"
BGN = "Begin"

DRW = "Draw"
ERR = "Error"
HARD = "Hard"
EASY = "Easy"

PLYR = "Player"
CMPTR = "Computer"
PLYRS_1 = "Two_players_1"
PLYRS_2 = "Two_players_2"

#Nujno mora biti vsaj en od COLLUMNS ali ROWS sod, drugace ni pošteno.
if not COLLUMNS * ROWS % 2 == 0 or COLLUMNS < 4 or ROWS < 4:
    assert False, "Napačne dimenzije tabele!"
#Spodnje kolicine morajo biti nizi, saj drugace bottle sprozi error.
if not(isinstance(PLYR, str) == isinstance(CMPTR, str) == isinstance(EASY, str) == isinstance(HARD, str) == isinstance(PLYRS_1, str) == isinstance(PLYRS_2, str)):
    assert False, "Te količine morajo biti nizi!"

class Game():
    board = [[EMPTY for _ in range(COLLUMNS)] for _ in range(ROWS)]
    
    def __init__(self, board, dificulty=HARD, player=PLYR):
        self.player = player
        self.dificulty = dificulty
        self.board = board
        if self.player == CMPTR:        #če začne računalnik, da svoj prvi žeton na sredino (=> lahko predpostavimo da vedno začne igralec)
                self.board[ROWS - 1][(COLLUMNS - 1) // 2] = CMPTR
                self.player = PLYR


    #PREVERJANJE ZMAGE

    #iskanje štirih v vrsto
    def row_of_four(self, row, collumn):
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
                    is_draw = False
                elif self.row_of_four(row, collumn) == PLYR:
                    return PLYR
                elif self.row_of_four(row,collumn) == CMPTR:
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

    #preveri če s potezo omogočimo/preprečimo zmago igralcu
    def smart_move(self, collumn):
        current_game_board = copy.deepcopy(self.board)
        self.board = Game.collumn_move(CMPTR, self.board, collumn)
        if not Game.move_is_possible(self.board, collumn):
            self.board = copy.deepcopy(current_game_board)
            return True
        else:
            self.board = Game.collumn_move(PLYR, self.board, collumn)
            if self.win() == PLYR:
                self.board = copy.deepcopy(current_game_board)
                return False
            else:
                self.board = copy.deepcopy(current_game_board)
                return True

    #poišče poteze, ki nam pripravijo 3 v vrsto (potencialno zmago)  
    def two_move_win_check(self):
        good_moves = set()
        current_game_board = copy.deepcopy(self.board)
        for collumn_1 in range(COLLUMNS):
            board_1 = copy.deepcopy(current_game_board)
            if Game.move_is_possible(board_1, collumn_1):
                board_1 = Game.collumn_move(CMPTR, board_1, collumn_1)
                for collumn_2 in range(COLLUMNS):
                    board_2 = copy.deepcopy(board_1)
                    if Game.move_is_possible(board_2, collumn_2):
                        self.board = Game.collumn_move(CMPTR, board_2, collumn_2)
                        if self.win() == CMPTR:
                            good_moves.add(collumn_1)
        self.board = copy.deepcopy(current_game_board)
        return good_moves

    #potezo računalnika razdelimo na tri dele, po tem, kakšno pomembnost ima možna poteza.
    
    #Pregledamo poteze, ki jih dobimo s funkcijo game_ending_moves
    def comptuer_move_1(self):
        choices_1 = self.game_ending_moves()
        if choices_1 == set():
            return "None" 
        for choice in choices_1:
            if choice[0] == CMPTR:
                collumn = choice[1]
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                return "end"
        for choice in choices_1:
            if choice[0] == PLYR:
                collumn = choice[1]
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                return "end"

    def computer_move_2(self):
        choices_2 = []
        for collumn in range(COLLUMNS):
            for row in range(ROWS):
                if self.board[row][collumn] != EMPTY:
                    choices_2.append(collumn)
        if len(choices_2) == 1:
            collumn = choices_2[0]
            if collumn == 0:
                self.board[ROWS - 1][3] = CMPTR
                return "end"
            elif collumn == COLLUMNS - 1:
                self.board[ROWS - 1][COLLUMNS - 4] = CMPTR
                return "end"
            elif collumn <= COLLUMNS // 2:
                self.board[ROWS - 1][collumn + 1] = CMPTR
                return "end"
            elif collumn > COLLUMNS // 2:
                self.board[ROWS - 1][collumn - 1] = CMPTR
                return "end"
            else:
                assert False, "Error?"
        choices_3 = self.two_move_win_check()
        if not choices_3 == set():
            collumn = random.sample(choices_3, 1)[0]
            if self.smart_move(collumn):
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                return "end"
        return "None"

    def computer_move_3(self):
        choices_4 = set()
        choices_5 = set()
        for collumn in range(COLLUMNS):
            if Game.move_is_possible(self.board, collumn):
                choices_5.add(collumn)
                if self.smart_move(collumn):
                    choices_4.add(collumn)
        if not choices_4 == set():
            collumn = random.sample(choices_4, 1)[0]
            self.board = Game.collumn_move(CMPTR, self.board, collumn)
            return "end"
        else:
            collumn = random.sample(choices_5, 1)[0]
            self.board = Game.collumn_move(CMPTR, self.board, collumn)
            return "end"
    
    def computer_move_main(self):
        if self.dificulty == HARD:
            test = self.comptuer_move_1()
            if test == "None":
                test = self.computer_move_2()
                if test == "None":
                    test = self.computer_move_3()
        elif self.dificulty == EASY:
            test = self.comptuer_move_1()
            if test == "None":
                test = self.computer_move_3()
        else:
            assert False, "Error?"


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
                self.computer_move_main()
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
        self.upload_game_from_file()
        game = Game(player=player, dificulty=dificulty, board=[[EMPTY for _ in range(COLLUMNS)] for _ in range(ROWS)])
        new_id = self.game_id_open()
        self.games[new_id] = (game, BGN)
        self.write_game_in_file()
        return new_id


    def move(self, game_id, collumn):
        self.upload_game_from_file()
        (game, _) = self.games[game_id]
        move = game.player_move(collumn)
        self.games[game_id] = (game, move)
        self.write_game_in_file()
        return
            
    def upload_game_from_file(self):
        with open(self.current_board_file) as file:
            encrypted_games = json.load(file) #Dobimo slovar z (geslom, crke)
            games = {}
            for game_id in encrypted_games:
                game = encrypted_games[game_id]
                games[int(game_id)] = (Game(board=game["board"], player=game["player"], dificulty=game["dificulty"]), game["move"])
            self.games = games
        return
    
    def write_game_in_file(self):
        with open(self.current_board_file, "w") as file:
            encrypted_games = {}
            for game_id in self.games:
                (game, move) = self.games[game_id]
                encrypted_games[game_id] = {"player": game.player, "dificulty": game.dificulty, "board": game.board, "move": move}
            json.dump(encrypted_games, file)
        return