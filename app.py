import socketio
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, send_from_directory

import util
import database
from affordle import Wordle

GAMES = []

affordle = Flask(__name__, static_url_path="", static_folder="affordle-webapp")
sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(sio, WsgiToAsgi(affordle))

# database.reset_databases()


@affordle.route("/")
def homepage():
    return send_from_directory(affordle.static_folder, 'index.html')


@sio.on("connect")
async def handle_connection(sid, *_):
    sio.enter_room(sid, room=sid)
    wlen = 5
    word_of_the_day = database.get_word_of_the_day(wlen)
    game = Wordle(sid, "bussy", wlen)
    GAMES.append(game)
    print(f"Connected + created game {sid}. {len(GAMES)} games in memory")


@sio.on("disconnect")
async def handle_disconnection(sid):
    util.remove_game_by_id(GAMES, sid)
    sio.leave_room(sid, room=sid)
    print(f"Disconnected {sid}, removed game. {len(GAMES)} left in memory")


@sio.on("req_resolve_guess")
async def resolve_guess(sid, guess):
    game = util.get_game_by_id(GAMES, sid)
    state, res = game.make_guess(guess)
    game_data = {"resolution": res, "state": str(state).split(".")[-1]}
    await sio.emit("resp_resolve_guess", game_data)
