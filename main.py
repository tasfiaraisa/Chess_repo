import tkinter as tk

###################### FUNCTIONS //////////////////////////////
def draw_chessboard(canvas):
    board_start_x = 50
    board_start_y = 100
    color = 'white'
    for row in range(8):  # There are 8 rows in a chessboard
        color = 'black' if color == 'white' else 'white'
        for col in range(8):  # There are 8 columns in a chessboard
            x1 = col * 100 + board_start_x  # Each square is 100x100 pixels
            y1 = row * 100 + board_start_y
            x2 = x1 + 100
            y2 = y1 + 100
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            color = 'black' if color == 'white' else 'white'


###################### CANVAS SET UP///////////////////////
main = tk.Tk()
main.geometry('900x1000')  # Adjust size to fit chessboard
main.title('Chess Game')

# Create canvas
canvas = tk.Canvas(main, bg='grey', width=900, height=1000)
canvas.pack()

# Draw chessboard
draw_chessboard(canvas)

# Start the main loop
main.mainloop()