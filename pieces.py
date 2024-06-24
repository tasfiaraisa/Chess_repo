from main import *

#Pieces moveset
#TO DO: Pawn, King, Queen, Rook, Bishop, Knight

##########################################################################################################################################

#Special move rules: 
    #Castling: give it to King, not Rook but give the rook one of the conditions of castling (havent moved yet), also the king is currently not in check or when no sqaures between king and rook is seen by any unfriendly pieces
    #En Passant: you know the rule, make it possible only one move
    #Pawn promotion: options at last row the pawn travels to - [queen, rook, bishop, knight]
    #Not being able to move if it puts u in check (king or any other piece)
    #Check: when king is in check, only allow specific moves that blocks the check or captures the checking piece
    #Checkmate: king not having legal squares to move to or any way of stopping itself from being captured

##########################################################################################################################################

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
        if board[startRow + direction][column - 1] is not None and whatColor(board[startRow + direction][column - 1]) != color:
            moves.append((startRow + direction, column - 1))

    #Captures to the right
    if column < 7:  #Ensure within the board limits
        if board[startRow + direction][column + 1] is not None and whatColor(board[startRow + direction][column + 1]) != color:
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
                    break  #Stop extending in this direction after a capture
                else:
                    break  #Stop if there is a piece of the same color
    
    return moves


# #

##########################################################################################################################################

# #Queen Moves
# #Code here
# def queenMoveset(position, color, board)




# #

##########################################################################################################################################

# #Rook Moves
# #Code here
# def rookMoveset(position, color, board)
    




# #

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




#

##########################################################################################################################################

# #Knight Moves
# #Code here
# def knightMoveset(position, color, board)





# #

##########################################################################################################################################

## Check for valid moves:

def isValidMove(currRow, currCol, row, column, piece):
    moves = []
    if abs(piece) == 1:
        moves = pawnMoveset(currRow, currCol, board, firstMove)
