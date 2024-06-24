import tkinter as tk
from pieces import kingMoveset, pawnMoveset, bishopMoveset, rookMoveset, queenMoveset, knightMoveset


board_start_x = 50
board_start_y = 10
square_size = 100
white = 100
black = 111
isPieceChosen = False #To check if the first mouse function has been selected or not
pieceChosen = 0
RowChosen = 0
colChosen = 0
WhiteTurn = True # To KEEP TRACK OF WHICH SIDE'S TURN IT IS 



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


######################################## FUNCTIONS ////////////////////////////////////////////////

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


## FUNCTION TO FIND KINGS POSITION
def find_king_position(board, color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.name == 'King' and piece.color == color:
                print(f"Found {color} King at ({row}, {col})")
                return (row, col)
    raise ValueError(f"{color} King not found on the board")


## GENERATE ALL POSSIBLE MOVES
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

## CHECK IF KING IS UNDER THREAT FROM NEW MOVE
def is_king_under_threat(board, color):
    king_position = find_king_position(board, color)
    opponent_color = white if color == black else black
    moves = generate_all_possible_moves(board, opponent_color)

    if king_position in moves:
        print(f"{color} King at {king_position} is in threat from {opponent_color}")
        return True
    print(f"{color} King at {king_position} is not in threat")
    return False

## CLICKING FUNCTION
def on_canvas_click(event):
    global isPieceChosen, RowChosen, colChosen, pieceChosen, WhiteTurn
    col = (event.x - board_start_x) // square_size
    row = (event.y - board_start_y) // square_size
    if 0 <= col < 8 and 0 <= row < 8:  # Ensure the click is within the bounds of the chessboard
        if not isPieceChosen: ## If no piece is chosen then u can choose new piece
            print(f"Clicked on row {row}, column {col}")
            pieceChosen = board[row][col]
            if pieceChosen is None:  ##If place selected is empty then return 
                return
            else:
                if WhiteTurn: ### CHECK WHICH SIDES TURN IT IS
                    if pieceChosen.color == black:
                        print("Not your turn")
                        pieceChosen = None
                        return 
                    else:
                        WhiteTurn = False
                
                elif not WhiteTurn:
                    if pieceChosen.color == white:
                        print("Not your turn")
                        pieceChosen = None
                        return 
                    else:
                        WhiteTurn = True
                ##Checking sides is done
                isPieceChosen = True #Turn piece chosen to true 
                RowChosen = row #Store the positions of the piece chosen 
                colChosen = col
                x1 = col * square_size + board_start_x
                y1 = row * square_size + board_start_y
                x2 = x1 + square_size
                y2 = y1 + square_size
                canvas.create_rectangle(x1, y1, x2, y2, fill='pink') ### SELECTED PIECE TURNS PINK
                symbol = get_piece_symbol(pieceChosen)
                if symbol:
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24), fill='white')
                return
        else: ## DESELECT THE PIECE 
            if row == RowChosen and col == colChosen: ##if new spot chosen is the same as previously selected piece
                isPieceChosen = False
                # Redraw the original square color
                x1 = colChosen * square_size + board_start_x ## get board coordinates
                y1 = RowChosen * square_size + board_start_y
                x2 = x1 + square_size
                y2 = y1 + square_size
                original_color = 'white' if (RowChosen + colChosen) % 2 == 0 else 'black'
                canvas.create_rectangle(x1, y1, x2, y2, fill=original_color)
                symbol = get_piece_symbol(board[RowChosen][colChosen])
                if symbol:
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol, font=('Arial', 24),
                                       fill='white' if original_color == 'black' else 'black') ## Draw the original color 
                    
                RowChosen = None
                colChosen = None
                pieceChosen = None
                WhiteTurn = not WhiteTurn ##Change White Turn to make sure after deselecting turn stays to the same player for they delected their move
                return
            else:
                # Check if move valid 
                valid_moves = []              
                if pieceChosen.name == 'King':
                    valid_moves = kingMoveset(RowChosen, colChosen, pieceChosen.color, board, pieceChosen.firstMove)

                elif pieceChosen.name == 'Pawn':
                    valid_moves = pawnMoveset(RowChosen, colChosen, pieceChosen.color, board, pieceChosen.firstMove)

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

                    ##Initialize castling bools
                    castlingMoveRight = False
                    castlingMoveLeft = False
                    prevkingUnderCheck = is_king_under_threat(board, pieceChosen.color) ##Initially was king under check 
                    if pieceChosen.name == 'King': ##Check on which side castling is occuring
                        if col == colChosen + 2:
                            castlingMoveRight = True 
                        elif col == colChosen - 2:
                            castlingMoveLeft = True

                    ##Move piece to new position
                    prev_piece = board[row][col]
                    board[row][col] = pieceChosen
                    board[RowChosen][colChosen] = None

                    ##Check if king is under threat after new move is made
                    kingUnderCheck = is_king_under_threat(board, pieceChosen.color)
                    if kingUnderCheck: ##If king is underthreat then that move is invalid
                        print("Invalid Move: King is under threat")
                        # Revert the move
                        board[row][col] = prev_piece
                        board[RowChosen][colChosen] = pieceChosen ##Move piece to original position 
                        isPieceChosen = False
                        RowChosen = None
                        colChosen = None
                        pieceChosen = None
                        WhiteTurn = not WhiteTurn
                        return
                    
                    else: ##If king not under threat after new move, proceed
                        
                        if castlingMoveRight: ## If castling then move the rook piece as wel 
                            if prevkingUnderCheck: ## Check if castling is occuring after check 
                                print("Invalid Move: King is under threat")
                                board[row][col] = prev_piece
                                board[RowChosen][colChosen] = pieceChosen ##Move piece to original position 
                                WhiteTurn = not WhiteTurn
                                return
                            else:
                                rookPiece = board[row][col + 1]
                                rookPiece.move(row, col - 1)
                                board[row][col + 1] = None
                                board[row][col - 1] = rookPiece

                        elif castlingMoveLeft:
                            if prevkingUnderCheck: ## Check if castling is occuring after check 
                                print("Invalid Move: King is under threat")
                                board[row][col] = prev_piece
                                board[RowChosen][colChosen] = pieceChosen ##Move piece to original position 
                                WhiteTurn = not WhiteTurn
                                return
                            else:
                                rookPiece = board[row][col - 2]
                                rookPiece.move(row, col + 1)
                                board[row][col - 2] = None
                                board[row][col + 1] = rookPiece
                
                    pieceChosen.move(row, col)
                    isPieceChosen = False ##Put all these back to null 
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