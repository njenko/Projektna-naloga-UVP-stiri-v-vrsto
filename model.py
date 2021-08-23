import copy
import random
import json

#število vrstic in stolpcev
COLLUMNS = 7
ROWS = 6

#Za lepši zapis kasneje
EMPTY = "Empty"
BGN = "Begin"

DRAW = "Draw"
ERR = "Error"
HARD = "Hard"
EASY = "Easy"

PLYR = "Player"
CMPTR = "Computer"
PLYRS_1 = "Two_players_1"
PLYRS_2 = "Two_players_2"


class Game:

    def __init__(self, board=[[EMPTY for _ in range(COLLUMNS)] for _ in range(ROWS)], dificulty=HARD, player=PLYR):
        self.player = player
        self.dificulty = dificulty
        self.board = board
        if self.player == CMPTR:    #če začne računalnik, da svoj prvi žeton na sredino (=> lahko predpostavimo da vedno začne igralec)
            self.board[ROWS - 1][(COLLUMNS - 1) // 2] = CMPTR
            self.player = PLYR


    #PREVERJANJE ZMAGE

    #iskanje štirih v vrsti
    def row_of_four(self, row, collumn):
        #iskati rabimo samo v te štiri smeri, ker bomo postore preverjali od spodaj navzgor in od leve proti desni
        directions = {(0, 1), (1, 1), (1, 0), (1, -1)} 
        starting_slot = self.board[row][collumn]
        if not starting_slot == EMPTY:
            for vec in directions:
                x, y = vec
                if 0 <= row + 3 * y < ROWS and  0 <= collumn + 3 * x < COLLUMNS:
                    if starting_slot == self.board[row + y][collumn + x] == self.board[row + 2 * y][collumn + 2 * x] == self.board[row + 3 * y][collumn + 3 * x]:
                        return starting_slot
        else:
            return EMPTY

    #preverjanje ali je igre konec => kdo je zmagovalec    
    def win(self):
        is_a_draw = True
        #pregledamo vsa polja od spodaj navzgor (manj pregledovanja).
        #Ko najdemo polje ki je del štirih zaporednih, vrnemo zmagovalca. Če takega polja ni igro nadaljujemo ali zaključimo z remijem, če ni več prostih polj.
        for row in range(ROWS):
            for collumn in range(COLLUMNS):
                if self.board[row][collumn] == EMPTY:
                    is_a_draw = False
                if self.row_of_four(row, collumn) == PLYR:
                    return PLYR
                elif self.row_of_four(row, collumn) == CMPTR:
                    return CMPTR
        if is_a_draw:
            return DRAW
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
                board[row][collumn] = player
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
        for collumn1 in range(COLLUMNS):
            board1 = copy.deepcopy(current_game_board)
            if Game.move_is_possible(board1, collumn1):
                board1 = Game.collumn_move(CMPTR, board1, collumn1)
                for collumn2 in range(COLLUMNS):
                    board2 = copy.deepcopy(board1)
                    if Game.move_is_possible(board2, collumn2):
                        self.board = Game.collumn_move(CMPTR, board2, collumn2)
                        if self.win() == CMPTR:
                            good_moves.add(collumn1)
        self.board = copy.deepcopy(current_game_board)
        return good_moves

    #potezo računalnika razdelimo na tri dele, po tem, kakšno pomembnost ima možna poteza.
    
    #Pregledamo poteze, ki jih dobimo s funkcijo game_ending_moves
    def computer_move_1(self):
        choices1 = self.game_ending_moves()
        if choices1 == set():
            return "none"
        for choice in choices1:
            if choice[0] == CMPTR:
                collumn = choice[1]
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                return "end"
        for choice in choices1:
            if choice[0] == PLYR:
                collumn = choice[1]
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                return "end"

    def computer_move_2(self):
        choices2 = []
        for collumn in range(COLLUMNS):
            for row in range(ROWS):
                if self.board[row][collumn] != EMPTY:
                    choices2.append(collumn)
        if len(choices2) == 1:
            collumn = choices2[0]
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
                assert False, "Do sem se nebi smelo dati priti."
        choices3 = self.two_move_win_check()
        if not choices3 == set():
            collumn = random.sample(choices3, 1)[0]
            if self.smart_move(collumn):
                self.board = Game.collumn_move(CMPTR, self.board, collumn)
                return "end"
        return "none"

    def computer_move_3(self):
        choices4 = set()
        choices5 = set()
        for collumn in range(COLLUMNS):
            if Game.move_is_possible(self.board, collumn):
                choices5.add(collumn)
                if self.smart_move(collumn):
                    choices4.add(collumn)
        if not choices4 == set():
            collumn = random.sample(choices4, 1)[0]
            self.board = Game.collumn_move(CMPTR, self.board, collumn)
            return "end"
        else:
            collumn = random.sample(choices5, 1)[0]
            self.board = Game.collumn_move(CMPTR, self.board, collumn)
            return "end"

    def computer_move_main(self):
        if self.dificulty == HARD:
            test = self.computer_move_1()
            if test == "none":
                test = self.computer_move_2()
                if test == "none":
                    test = self.computer_move_3()
        elif self.dificulty == EASY:
            test = self.computer_move_1()
            if test == "none":
                test = self.computer_move_3()
        else:
            assert False, "Do sem se nebi smelo dati priti."


    #POTEZA IGRALCA

    #Poteza igralca v igri proti računalniku
    def single_player_move(self, collumn): 
        board = copy.deepcopy(self.board)
        if not Game.move_is_possible(board, collumn):
            return ERR
        else:
            self.board = Game.collumn_move(PLYR, self.board, collumn)
            outcome = self.win()
            if outcome == PLYR or outcome == DRAW:
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
            assert False, "Do sem se nebi smelo dati priti."

    #funkcija, ki jo kličemo vedno, ko je na potezi igralec
    def move(self, collumn):
        if self.player == PLYRS_1 or self.player == PLYRS_2:
            return self.two_player_move(collumn)
        else:
            return self.single_player_move(collumn)



class ActiveGame:
    def __init__(self, game_file):
        self.game_file = game_file
        self.games = {}

    def id_is_free(self):
        if self.games == {}:
            return 0
        else:
            for i in range(len(self.games) + 1):
                if i not in self.games.keys():
                    return i
    
    def new_game(self, player=PLYR, dificulty=HARD):
        self.download_game_from_file()
        game = Game(player=player, dificulty=dificulty, board=[[EMPTY for _ in range(COLLUMNS)] for _ in range(ROWS)])
        new_id = self.id_is_free()
        self.games[new_id] = (game, BGN)
        self.write_game_to_file()
        return new_id

    def move(self, game_id, collumn):
        self.download_game_from_file()
        (game, _) = self.games[game_id]
        move = game.move(collumn)
        self.games[game_id] = (game, move)
        self.write_game_to_file()
        return

    def download_game_from_file(self):
        with open(self.game_file) as file:
            encrypted_games = json.load(file) #Dobimo slovar z (geslom, crke)
            games = {}
            for game_id in encrypted_games:
                game = encrypted_games[game_id]
                games[int(game_id)] = (Game(board=game["board"], player=game["player"], dificulty=game["dificulty"]), game["move"])
            self.games = games
        return

    def write_game_to_file(self):
        with open(self.game_file, "w") as file:
            encrypted_games = {}
            for game_id in self.games:
                (game, move) = self.games[game_id]
                encrypted_games[game_id] = {"player": game.player, "dificulty": game.dificulty, "board": game.board, "move": move}
            json.dump(encrypted_games, file)
        return