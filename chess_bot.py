## CHESS ENGINE 
from pieces import checkMate, staleMate 

pieces_values = {'Pawn' : 1, 'Rook' : 5, 'Knight' : 3, 'Bishop' : 3, 'Queen' : 9, 'King' : 0}
WHITE = 100
BLACK = 111

class Move:
    def __init__(self, start_row, start_col, end_row, end_col, piece_moved, piece_captured=None):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.promotion = False

def evaluateBoard(board):
    if is_checkMate(board, WHITE):
        return -10000

    if is_checkMate(board, BLACK):
        return 10000
    if is_staleMate(board, WHITE):
        return 0

    if is_staleMate(board, BLACK):
        return 0
     
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.name in pieces_values:
                if piece.color == 111: ##BLACK
                    score += pieces_values[piece.name]
                elif piece.color == 100: ##WHITE
                    score -= pieces_values[piece.name]

    return score

def make_move(board, move):
    move.piece_captured = board[move.end_row][move.end_col]
    piece = board[move.start_row][move.start_col]
    board[move.end_row][move.end_col] = piece
    board[move.start_row][move.start_col] = None

    if piece.name == 'Pawn' and (move.end_row == 0 or move.end_row == 7):
        piece.name = 'Queen'
        move.promotion = True

    return 

def undo_move(board, move):
    piece = board[move.end_row][move.end_col]
    board[move.start_row][move.start_col] = piece
    board[move.end_row][move.end_col] = move.piece_captured

    if move.promotion is True:
        piece.name = 'Pawn'

    return 







    