from flask import *
import json
import chess

def filter_moves_on_piece(moves, square):
    moves_ls = [str(move) for move in moves]
    new = []
    valid = []
    for i in moves_ls:
        j = chess.BaseBoard().piece_at(chess.parse_square(i[:2]))
        new.append(str(j) + i[-2:])
        for k in new:
            print(k)
            if square in k:
                valid.append(k)

    return json.dumps({moves: valid})

# create the app
app = Flask(__name__)


# start the board
board = chess.Board()

@app.route('/', methods=['POST', 'GET'])
def homepage():
    with open('website/index.html', 'r') as f:
        return f.read()

@app.route('/moves/<square>')
def get_moves(square):
    legal_moves = board.legal_moves
    return filter_moves_on_piece(legal_moves, square)

@app.route('/state')
def state():
    return json.dumps({'board': str(str(board).replace(" ", "")).replace("\n", "V")})

@app.route('/move/{squareStart}-{squareEnd}')
def make_move(squareStart, squareEnd):
    try:
        board.push(chess.Move.from_uci(f"{squareStart.lower()}{squareEnd.lower()}"))
    except Exception as e:
        return 500, f"{squareStart.lower()}{squareEnd.lower()} is an invalid uci"
    return 200, state()

@app.route('/assets/<path:path>')
def get_assets(path):
    with open(f'website/assets/{path}', 'rb') as f:
        return f.read()

if __name__ == '__main__':
    app.run()
