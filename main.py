import tkinter as tk
from pieces import *


board_start_x = 50
board_start_y = 100
square_size = 100
white = 100
black = 111
isPieceChosen = False #To check if the first mouse function has been selected or not
pieceChosen = 0
RowChosen = 0
colChosen = 0


###################### CLASSES /////////////////////////////////

class ChessPiece:
    def __init__(self, name, row, column, color):
        self.name = name
        self.row = row
        self.column = column 
        self.color = color 
        self.firstMove = True

    def move(self, new_row, new_column):
        self.row = new_row
        self.column = new_column
        self.firstMove = False


###################### FUNCTIONS //////////////////////////////

def initialize_board():
    
    # Initialize the board with None
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place pawns
    for i in range(8):
        board[1][i] = ChessPiece('Pawn', 1, i, white)  # White pawns
        board[6][i] = ChessPiece('Pawn', 6, i, black)  # Black pawns

    # Define the other pieces
    piece_order = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
    
    # Place pieces on row 0 for white and row 7 for black
    for i, piece_name in enumerate(piece_order):
        board[0][i] = ChessPiece(piece_name, 0, i, white)  # White pieces
        board[7][i] = ChessPiece(piece_name, 7, i, black)  # Black pieces

    return board

# function that will be changed to images later
def get_piece_symbol(piece):
    if piece is None:
        return ' '
    
    white_symbols = {'Pawn': '♙', 'Knight': '♘', 'Bishop': '♗', 'Rook': '♖', 'Queen': '♕', 'King': '♔'}
    
    black_symbols = {'Pawn': '♟', 'Knight': '♞', 'Bishop': '♝', 'Rook': '♜', 'Queen': '♛', 'King': '♚'}
    
    if piece.color == white:
        return white_symbols[piece.name]
    
    if piece.color == black:
        return black_symbols[piece.name]



def draw_chessboard(canvas, board):
    for row in range(8):
        for col in range(8):
            x1 = col * square_size + board_start_x
            y1 = row * square_size + board_start_y
            x2 = x1 + square_size
            y2 = y1 + square_size
            color = 'white' if (row + col) % 2 == 0 else 'black'
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            # get piece
            piece = board[row][col]
            symbol = get_piece_symbol(piece)
            if symbol:  
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24), fill='white' if color == 'black' else 'black')

def on_canvas_click(event):
    global isPieceChosen, RowChosen, colChosen, pieceChosen 
    col = (event.x - board_start_x) // square_size
    row = (event.y - board_start_y) // square_size
    if 0 <= col < 8 and 0 <= row < 8:  # Ensure the click is within the bounds of the chessboard
        if isPieceChosen == False:
            print(f"Clicked on row {row}, column {col}")
            pieceChosen = board[row][col]
            if pieceChosen is None:
                return
            else:
                isPieceChosen = True
                RowChosen = row
                colChosen = col
                x1 = col * square_size + board_start_x
                y1 = row * square_size + board_start_y
                x2 = x1 + square_size
                y2 = y1 + square_size
                canvas.create_rectangle(x1, y1, x2, y2, fill='pink')
                symbol = get_piece_symbol(pieceChosen)
                if symbol:  
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24), fill='white')
                    return 

        if isPieceChosen == True:
                if(row == RowChosen & col == colChosen):
                    isPieceChosen = False
                    x1 = col * square_size + board_start_x
                    y1 = row * square_size + board_start_y
                    x2 = x1 + square_size
                    y2 = y1 + square_size
                    color = 'white' if (row + col) % 2 == 0 else 'black'
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                    symbol = get_piece_symbol(pieceChosen)
                    if symbol:  
                        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24), fill='white')
                    return 
                # Moving the peice or checking if the piece is valid or not 
                else:
                    isPieceChosen == False
                    color = board[RowChosen][colChosen].color
                    isFirst = board[RowChosen][colChosen].firstMove #Checking if its the piece's first move or not
                    moves = pawnMoveset(row, col, color, board, isFirst)
                    size = moves.len()
                    for i in range(size):
                        if((row, col) == moves(i)):
                            piece = board[row][col]
                            piece.move(row, col)
                            board[row][col] = piece
                            board[RowChosen][colChosen] = None
                            draw_chessboard(canvas, board)
                            return 

       

def choose_move(event):
    isPieceChosen = False
    col = (event.x - board_start_x) // square_size
    row = (event.y - board_start_y) // square_size
    if 0 <= col < 8 and 0 <= row < 8:  # Ensure the click is within the bounds of the chessboard
        if(row == RowChosen & col == colChosen):
            isPieceChosen = False
            x1 = col * square_size + board_start_x
            y1 = row * square_size + board_start_y
            x2 = x1 + square_size
            y2 = y1 + square_size
            color = 'white' if (row + col) % 2 == 0 else 'black'
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            symbol = get_piece_symbol(pieceChosen)
            if symbol:  
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24), fill='white')
            return 
        


def whatColor(row, column):
    piece = board[row][column]
    color = piece.color
    return color 
    


###################### CANVAS SET UP ///////////////////////
main = tk.Tk()
main.geometry('1000x1000')  # Adjust size to fit chessboard
main.title('Chess Game')

# Create canvas
canvas = tk.Canvas(main, bg='grey', width=900, height=900)
canvas.pack()
canvas.bind("<Button-1>", on_canvas_click)



######################### MAIN ///////////////////////////
# Draw chessboard

board = initialize_board()
draw_chessboard(canvas, board)

# Start the main loop
main.mainloop()