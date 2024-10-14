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

################################################### PIECES.PY ############################################################

#Castling
def castling(row, col, board, rookFirstMove, side):
    moves = []

    if rookFirstMove:
        if side == 0:  # LEFT SIDE (Queen's side castling)
            if all(board[row][c] is None for c in range(col - 1, col - 4, -1)):
                moves.append((row, col - 2))
        elif side == 1:  # RIGHT SIDE (King's side castling)
            if all(board[row][c] is None for c in range(col + 1, col + 3)):
                moves.append((row, col + 2))
    
    return moves    

def can_CastleKingside(king, board):
    if king.has_moved or board[king.row][7] is None or board[king.row][7].has_moved:
        return False
    if any(board[king.row][i] for i in range(king.col + 1, 7)):
        return False
    if any(is_square_under_attack(board, king.row, i, king.color) for i in range(king.col, king.col + 3)):
        return False
    return True

def can_CastleQueenside(king, board):
    if king.has_moved or board[king.row][0] is None or board[king.row][0].has_moved:
        return False
    if any(board[king.row][i] for i in range(1, king.col)):
        return False
    if any(is_square_under_attack(board, king.row, i, king.color) for i in range(king.col - 2, king.col + 1)):
        return False
    return True


###################################################################################################################
#Pawn Moves
#to be checked, not done yet
def pawnMoveset(row, col, color, board, firstMove):
    moves = []
    #Determines moving direction
    direction = 1 if color == 111 else -1
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

#Promotion
def pawnPromotion(row, col, board, color):
    # Check for pawn reaching the last row
    promotionRow = 0 if color == 100 else 7
    if row == promotionRow:
        return True  # Returns True if pawn needs promotion
    return False

def promotePawn(row, col, board, promotion_choice='Queen'):
    # Ensure the pawn at the location can be promoted
    if not pawnPromotion(row, col, board, board[row][col].color):
        return  # No promotion if not on the correct row

    createNewPiece = board[row][col]
    if createNewPiece.name == 'Pawn':
        if promotion_choice == 'Queen':
            board[row][col] = Queen(createNewPiece.color)  # Assuming Queen class is defined
        elif promotion_choice == 'Rook':
            board[row][col] = Rook(createNewPiece.color)  # Assuming Rook class is defined
        elif promotion_choice == 'Bishop':
            board[row][col] = Bishop(createNewPiece.color)  # Assuming Bishop class is defined
        elif promotion_choice == 'Knight':
            board[row][col] = Knight(createNewPiece.color)  # Assuming Knight class is defined


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
            moves.extend(castling(row, col, board, rookFirstMoveLeft, 0))  # Queen's side castling

        if board[row][7] is not None and board[row][7].name == 'Rook':
            rookFirstMoveRight = board[row][7].firstMove
            moves.extend(castling(row, col, board, rookFirstMoveRight, 1))  # King's side castling


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


##########################################################################################################################################

# #En Passant logic
def en_passant(pawn, board, last_move):
    if last_move.piece.name == 'Pawn' and abs(last_move.start_row - last_move.end_row) == 2:
        if pawn.row == last_move.end_row and abs(pawn.col - last_move.end_col) == 1:
            # En passant is possible, set up capture mechanics in your game state
            return True
    return False

##########################################################################################################################################
