import tkinter as tk

###################### FUNCTIONS //////////////////////////////

def initialize_board():
    board = [
        [4, 2, 3, 5, 6, 3, 2, 4],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-4, -2, -3, -5, -6, -3, -2, -4]
    ]
    return board

# function that will be changed to images later
def get_piece_symbol(piece):
    symbols = {
        1: '♙', 2: '♘', 3: '♗', 4: '♖', 5: '♕', 6: '♔',
        -1: '♟', -2: '♞', -3: '♝', -4: '♜', -5: '♛', -6: '♚',
        0: ''
    }
    return symbols[piece]


def draw_chessboard(canvas, board):
    board_start_x = 50
    board_start_y = 100
    square_size = 100
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



###################### CANVAS SET UP ///////////////////////
main = tk.Tk()
main.geometry('1000x1000')  # Adjust size to fit chessboard
main.title('Chess Game')

# Create canvas
canvas = tk.Canvas(main, bg='grey', width=900, height=900)
canvas.pack()


######################### MAIN ///////////////////////////
# Draw chessboard

board = initialize_board()
draw_chessboard(canvas, board)

# Start the main loop
main.mainloop()