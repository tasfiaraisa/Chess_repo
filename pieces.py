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
def castling(king, board, kingside=True):
    if king.has_moved:
        return False  # Cannot castle if the king has already moved

    # Set parameters based on kingside or queenside castling
    direction = 1 if kingside else -1
    rook_col = 7 if kingside else 0
    step = 1 if kingside else -1
    check_positions = range(king.col + step, rook_col, step)
    final_king_pos = king.col + 2 * direction
    final_rook_pos = king.col + direction

    # Ensure the rook exists and hasn't moved
    rook = board[king.row][rook_col]
    if rook is None or rook.has_moved:
        return False

    # Ensure there are no pieces between the king and the rook
    if any(board[king.row][pos] for pos in check_positions):
        return False

    # Ensure no positions the king crosses are under attack
    for pos in range(king.col, final_king_pos + direction, direction):
        if is_square_under_attack(board, king.row, pos, king.color):
            return False

    # Move the king and rook
    board[king.row][king.col], board[king.row][final_king_pos] = None, king
    board[king.row][rook_col], board[king.row][final_rook_pos] = None, rook
    king.has_moved = rook.has_moved = True
    return True

def is_square_under_attack(board, row, col, color):
    # Placeholder for checking if a square is under attack
    # You would need to implement this based on your game logic
    pass



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
# #for the human player
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
            board[row][col] = Queen(createNewPiece.color)
        elif promotion_choice == 'Rook':
            board[row][col] = Rook(createNewPiece.color)
        elif promotion_choice == 'Bishop':
            board[row][col] = Bishop(createNewPiece.color)
        elif promotion_choice == 'Knight':
            board[row][col] = Knight(createNewPiece.color)

# #for the bot player
def promotePawnBot(row, col, board, color, promotion_choice=None):
    if not pawnPromotion(row, col, board, color):
        return  # No promotion if the pawn is not on the correct row
    
    # AI or strategy-based decision for promotion, if not specified
    if not promotion_choice:
        promotion_choice = decidePromotionPiece(board, color)
    
    # Create a new piece based on the promotion choice
    if promotion_choice == 'Queen':
        board[row][col] = Queen(color)
    elif promotion_choice == 'Rook':
        board[row][col] = Rook(color)
    elif promotion_choice == 'Bishop':
        board[row][col] = Bishop(color)
    elif promotion_choice == 'Knight':
        board[row][col] = Knight(color)

def decidePromotionPiece(board, color):
    return 'Queen'


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
