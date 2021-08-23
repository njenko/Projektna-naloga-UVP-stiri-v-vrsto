import bottle, model

active_game = model.ActiveGame("stanje.json")
SECRET_KEY = "Hello, 'tis me, the secret key"


#začetna stran
@bottle.get('/')
def front_page():
    return bottle.template('site/index.tpl')


#reset
@bottle.post('/')
def reset():
    bottle.redirect('/')
    return


#gumb za začnejanje nove igre
@bottle.post('/new_game/<player>/<dificulty>')
def start_new_game(player, dificulty):
    #POST naredi novo igro, reusmeri na naslov za igranje te nove igre
    #igro proti računalniku začne igralec 
    if player == model.PLYR and dificulty == model.EASY:
        game_id = active_game.new_game(player=model.PLYR, dificulty=model.EASY)
    elif player == model.PLYR and dificulty == model.HARD:
        game_id = active_game.new_game(player=model.PLYR, dificulty=model.HARD)
    #igro proti računalniku začne računalnik
    elif player == model.CMPTR and dificulty == model.EASY:
        game_id = active_game.new_game(player=model.CMPTR, dificulty=model.EASY)
    elif player == model.CMPTR and dificulty == model.HARD:
        game_id = active_game.new_game(player=model.CMPTR, dificulty=model.HARD)
    #igra z dvema igralcema
    elif player == model.PLYRS_1 and dificulty == model.HARD:
        game_id = active_game.new_game(player=model.PLYRS_1, dificulty=model.HARD)
    else:
        assert False, "Do sem se nebi smelo dati priti."
    bottle.response.set_cookie("game_id", game_id, secret=SECRET_KEY, path="/")
    bottle.redirect('/game/')
    return


#moramo preusmeriti na GET, da ne izgubimo vsega, ko osvežimo stran
@bottle.get('/game/')
def show_game():
    game_id = bottle.request.get_cookie("game_id", secret=SECRET_KEY)
    (game, move) = active_game.games[game_id]
    return bottle.template('site/game.tpl', game=game, game_id=game_id, move=move)


@bottle.post("/make_a_move/<n:int>")
def make_a_move(n):
    collumn = n
    game_id = bottle.request.get_cookie("game_id", secret=SECRET_KEY)
    active_game.move(game_id, collumn)
    bottle.redirect('/game/')
    return


#slike
@bottle.get("/static/<filename>")
def server_static(filename):
    return bottle.static_file(filename, root="./images")


bottle.run(reloader=True, debug=True)