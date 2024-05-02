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
def pawnMoveset(position, color, board, firstMove):
    moves = []
    #Determines moving direction
    direction = 1 if color == 'white' else -1
    startRow = position[0]
    column = position[1]

    #Move forward one square
    if board[startRow + direction][column] == '--':  #empty square is represented as '--'
        moves.append((startRow + direction, column))
        #Move forward two squares from the starting position
        if firstMove and board[startRow + 2 * direction][column] == '--':
            moves.append((startRow + 2 * direction, column))

    #Captures to the left
    if column > 0:  #Ensure within the board limits
        if board[startRow + direction][column - 1] != '--' and board[startRow + direction][column - 1][0] != color[0]:
            moves.append((startRow + direction, column - 1))

    #Captures to the right
    if column < 7:  #Ensure within the board limits
        if board[startRow + direction][column + 1] != '--' and board[startRow + direction][column + 1][0] != color[0]:
            moves.append((startRow + direction, column + 1))

    return moves

##########################################################################################################################################

# #King Moves
# #Code here 
# def kingMoveset(position, color, board, firstMove)



# #

##########################################################################################################################################

# #Queen Moves
# #Code here
# def queenMoveset(position, color, board, firstMove)




# #

##########################################################################################################################################

# #Rook Moves
# #Code here
# def rookMoveset(position, color, board, firstMove)
    




# #

##########################################################################################################################################

# #Bishop Moves
# #Code here
# def bishopMoveset(position, color, board, firstMove)





# #

##########################################################################################################################################

# #Knight Moves
# #Code here
# def knightMoveset(position, color, board, firstMove)





# #

##########################################################################################################################################






