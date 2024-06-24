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



def draw_chessboard(board):
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


################################################### PIECES.PY ############################################################

#Castling
def castling(row, col, rookFirstMove, side):
    moves = []

    if rookFirstMove:
        if side == 0:  # LEFT SIDE (Queen's side castling)
            if all(board[row][c] is None for c in range(col - 1, col - 4, -1)):
                moves.append((row, col - 2))
        elif side == 1:  # RIGHT SIDE (King's side castling)
            if all(board[row][c] is None for c in range(col + 1, col + 3)):
                moves.append((row, col + 2))
    
    return moves    



###################################################################################################################
#Pawn Moves
#to be checked, not done yet
def pawnMoveset(row, col, color, board, firstMove):
    moves = []
    #Determines moving direction
    direction = 1 if color == 'white' else -1
    startRow = row
    column = col

    #Move forward one square
    if board[startRow + direction][column] is None:  #empty square is represented as 0
        moves.append((startRow + direction, column))
        #Move forward two squares from the starting position
        if firstMove and board[startRow + 2 * direction][column] == None:
            moves.append((startRow + 2 * direction, column))

    #Captures to the left
    if column > 0:  #Ensure within the board limits
        if board[startRow + direction][column - 1] is not None and board[startRow + direction][column - 1].color != color:
            moves.append((startRow + direction, column - 1))

    #Captures to the right
    if column < 7:  #Ensure within the board limits
        if board[startRow + direction][column + 1] is not None and board[startRow + direction][column + 1].color != color:
            moves.append((startRow + direction, column + 1))

    return moves

##########################################################################################################################################

# #King Moves
# #Code here 
def kingMoveset(row, col, color, board, firstMove):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0)]  
    #Check each of the possible directions
    for d in directions:
            newRow, newCol = row + d[0], col + d[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:  #Ensure that the position is still on the board
                if board[newRow][newCol] is None:  #The square is empty
                    moves.append((newRow, newCol))
                elif board[newRow][newCol].color != color:  #The square contains an enemy piece
                    moves.append((newRow, newCol))
    
    if firstMove:
        # Assume left rook is at col 0 and right rook is at col 7
        if board[row][0] is not None and board[row][0].name == 'Rook':
            rookFirstMoveLeft = board[row][0].firstMove
            moves.extend(castling(row, col, rookFirstMoveLeft, 0))  # Queen's side castling

        if board[row][7] is not None and board[row][7].name == 'Rook':
            rookFirstMoveRight = board[row][7].firstMove
            moves.extend(castling(row, col, rookFirstMoveRight, 1))  # King's side castling


    return moves


##########################################################################################################################################

#Bishop Moves
#Code here
def bishopMoveset(row, col, color, board):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  #Diagonal movements: top-left, top-right, bottom-left, bottom-right

    #Check each of the four possible diagonal directions
    for d in directions:
        for i in range(1, 8):  #bishop can move up to 7 squares in each direction
            newRow, newCol = row + d[0] * i, col + d[1] * i
            if 0 <= newRow < 8 and 0 <= newCol < 8:  #Ensure that the position is still on the board
                if board[newRow][newCol] is None:  #The square is empty
                    moves.append((newRow, newCol))
                elif board[newRow][newCol].color != color:  #The square contains an enemy piece
                    moves.append((newRow, newCol))
                    break  #Stop extending in this direction after a capture
                else:
                    break  #Stop if there is a piece of the same color
            else:
                break  #Stop if out of board bounds

    return moves

##########################################################################################################################################

# #Rook Moves
# #Code here
def rookMoveset(row, col, color, board, firstMove):
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    #Check each of the four possible horizontal and vertical directions
    for d in directions:
        for i in range(1, 8):  #bishop can move up to 7 squares in each direction
            newRow, newCol = row + d[0] * i, col + d[1] * i
            if 0 <= newRow < 8 and 0 <= newCol < 8:  #Ensure that the position is still on the board
                if board[newRow][newCol] is None:  #The square is empty
                    moves.append((newRow, newCol))
                elif board[newRow][newCol].color != color:  #The square contains an enemy piece
                    moves.append((newRow, newCol))
                    break  #Stop extending in this direction after a capture
                else:
                    break  #Stop if there is a piece of the same color
            else:
                break  #Stop if out of board bounds

    return moves



##########################################################################################################################################

# #Queen Moves
# #Code here
def queenMoveset(row, col, color, board):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0)]  

    #Check for all possible directions 
    for d in directions:
        for i in range(1, 8):  #bishop can move up to 7 squares in each direction
            newRow, newCol = row + d[0] * i, col + d[1] * i
            if 0 <= newRow < 8 and 0 <= newCol < 8:  #Ensure that the position is still on the board
                if board[newRow][newCol] is None:  #The square is empty
                    moves.append((newRow, newCol))
                elif board[newRow][newCol].color != color:  #The square contains an enemy piece
                    moves.append((newRow, newCol))
                    break  #Stop extending in this direction after a capture
                else:
                    break  #Stop if there is a piece of the same color
            else:
                break  #Stop if out of board bounds

    return moves

##########################################################################################################################################

# #Knight Moves
# #Code here
def knightMoveset(row, col, color, board):
    moves = []
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    for d in directions:
            newRow, newCol = row + d[0], col + d[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:  #Ensure that the position is still on the board
                if board[newRow][newCol] is None:  #The square is empty
                    moves.append((newRow, newCol))
                elif board[newRow][newCol].color != color:  #The square contains an enemy piece
                    moves.append((newRow, newCol))
    
    return moves


##########################################################################################################################
##########################################################################################################################


def find_king_position(board, color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.name == 'King' and piece.color == color:
                print(f"Found {color} King at ({row}, {col})")
                return (row, col)
    raise ValueError(f"{color} King not found on the board")

def generate_all_possible_moves(board, color):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.color == color:
                if piece.name == 'Pawn':
                    moves.extend(pawnMoveset(row, col, piece.color, board, piece.firstMove))
                elif piece.name == 'Bishop':
                    moves.extend(bishopMoveset(row, col, piece.color, board))
                elif piece.name == 'Rook':
                    moves.extend(rookMoveset(row, col, piece.color, board, piece.firstMove))
                elif piece.name == 'Queen':
                    moves.extend(queenMoveset(row, col, piece.color, board))
                elif piece.name == 'Knight':
                    moves.extend(knightMoveset(row, col, piece.color, board))
                elif piece.name == 'King':
                    moves.extend(kingMoveset(row, col, piece.color, board, piece.firstMove))
    print(f"Generated {len(moves)} moves for {color}")
    return moves

def is_king_under_threat(board, color):
    king_position = find_king_position(board, color)
    opponent_color = white if color == black else black
    moves = generate_all_possible_moves(board, opponent_color)

    if king_position in moves:
        print(f"{color} King at {king_position} is in threat from {opponent_color}")
        return True
    print(f"{color} King at {king_position} is not in threat")
    return False

def on_canvas_click(event):
    global isPieceChosen, RowChosen, colChosen, pieceChosen
    col = (event.x - board_start_x) // square_size
    row = (event.y - board_start_y) // square_size
    if 0 <= col < 8 and 0 <= row < 8:  # Ensure the click is within the bounds of the chessboard
        if not isPieceChosen:
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
        else: ## DESELECT THE PIECE 
            if row == RowChosen and col == colChosen:
                isPieceChosen = False
                # Redraw the original square color
                x1 = colChosen * square_size + board_start_x
                y1 = RowChosen * square_size + board_start_y
                x2 = x1 + square_size
                y2 = y1 + square_size
                original_color = 'white' if (RowChosen + colChosen) % 2 == 0 else 'black'
                canvas.create_rectangle(x1, y1, x2, y2, fill=original_color)
                symbol = get_piece_symbol(board[RowChosen][colChosen])
                if symbol:
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24),
                                       fill='white' if original_color == 'black' else 'black')
                    
                RowChosen = None
                colChosen = None
                pieceChosen = None
                return
            else:
                # Check if move valid 
                valid_moves = []              
                if pieceChosen.name == 'King':
                    valid_moves = kingMoveset(RowChosen, colChosen, pieceChosen.color, board, pieceChosen.firstMove)

                elif pieceChosen.name == 'Pawn':
                    valid_moves = kingMoveset(RowChosen, colChosen, pieceChosen.color, board, pieceChosen.firstMove)

                elif pieceChosen.name == 'Bishop':
                    valid_moves = bishopMoveset(RowChosen, colChosen, pieceChosen.color, board)
                
                elif pieceChosen.name == 'Rook':
                    valid_moves = rookMoveset(RowChosen, colChosen, pieceChosen.color, board, pieceChosen.firstMove)

                elif pieceChosen.name == 'Queen':
                    valid_moves = queenMoveset(RowChosen, colChosen, pieceChosen.color, board)

                elif pieceChosen.name == 'Knight':
                    valid_moves = knightMoveset(RowChosen, colChosen, pieceChosen.color, board)

                if (row, col) in valid_moves:

                    # Move the piece
                    castlingMoveRight = False
                    castlingMoveLeft = False
                    if pieceChosen.name == 'King':
                        if col == colChosen + 2:
                            castlingMoveRight = True 
                        elif col == colChosen - 2:
                            castlingMoveLeft = True

                    prev_piece = board[row][col]
                    board[row][col] = pieceChosen
                    board[RowChosen][colChosen] = None

                    kingUnderCheck = is_king_under_threat(board, pieceChosen.color)
                    if kingUnderCheck:
                        print("Invalid Move: King is under threat")
                        # Revert the move
                        board[row][col] = prev_piece
                        board[RowChosen][colChosen] = pieceChosen
                        isPieceChosen = False
                        RowChosen = None
                        colChosen = None
                        pieceChosen = None
                        return
                    
                    else:
                        pieceChosen.move(row, col)
                        if castlingMoveRight:
                            rookPiece = board[row][col + 1]
                            rookPiece.move(row, col - 1)
                            board[row][col + 1] = None
                            board[row][col - 1] = rookPiece

                        elif castlingMoveLeft:
                            rookPiece = board[row][col - 2]
                            rookPiece.move(row, col + 1)
                            board[row][col - 2] = None
                            board[row][col + 1] = rookPiece
                
                    
                    isPieceChosen = False
                    RowChosen = None
                    colChosen = None
                    pieceChosen = None
                    draw_chessboard(board)
               
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
draw_chessboard(board)

# Start the main loop
main.mainloop()