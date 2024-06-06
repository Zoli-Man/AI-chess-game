import random
import noUI
from noUI import Piece_type
from noUI import Color
import chess_ai

# convert the board to a list of lists, where each element is the value of the piece in the board at that location (0 if empty)
# mapping: queen = 1 ,king = 2, rook = 3, bishop = 4, knight = 5, pawn = 6 black = positive, white = negative
def board_to_list(board):
    list = [[0]*8 for i in range(8)]
    for location, piece in board.pieces.items():
        x, y = location
        list[x][y] = piece.piece_type.value if piece.color == Color.BLACK else -1*piece.piece_type.value
    return list

def board_to_list_of_move_count_of_pice(board):
    list = [[0]*8 for i in range(8)]
    for location, piece in board.pieces.items():
        x, y = location
        list[x][y] = piece.move_count
    return list
def board_to_list_of_pawn_double_move(board):
    list = [[0]*8 for i in range(8)]
    for location, piece in board.pieces.items():
        x, y = location
        if piece.piece_type.value == 6:
            list[x][y] = piece.pawn_double_move_at_turn
    return list

def chose_move2(board):
    return chess_ai.best_move(board_to_list(board), board_to_list_of_move_count_of_pice(board), board_to_list_of_pawn_double_move(board),board.move_count)

def chose_move(board):
    """moves = []
    for location in board.black_locations:
        moves += board.get_move_for_location(location)
    move = random.choice(moves) if moves !=[] else None"""
    #print(get_piece_count(board))
    #print(val_function(board))
    print("test")
    #chose_move2(board)
    print("test_end")

    #todo: add a get_all_moves function to the board class
    #todo: use +- inf instead of 1000000
    moves = board.get_all_moves(Color.BLACK)
    if moves == []:
        return None
    best_move, val =None , -1000000
    for move in moves:
        child = board.creat_child_bord(move)
        eval = minmax(child, 1, -1000000, 1000000, False)
        if eval > val:
            best_move ,val = move, eval



    return best_move


def get_piece_count(board):
    list = [0]*10
    for piece in board.pieces.values():
        piece_type_val = piece.piece_type.value
        piece_color = piece.color.value
        if piece_color == 1: #white
            if piece_type_val == 6: #pawn
                list[0] += 1
            elif piece_type_val == 5: #knight
                list[1] += 1
            elif piece_type_val == 4: #bishop
                list[2] += 1
            elif piece_type_val == 3: #rook
                list[3] += 1
            elif piece_type_val == 1: #queen
                list[4] += 1

        else: #black
            if piece_type_val == 6: #pawn
                list[5] += 1
            elif piece_type_val == 5: #knight
                list[6] += 1
            elif piece_type_val == 4:  # bishop
                list[7] += 1
            elif piece_type_val == 3: # rook
                list[8] += 1
            elif piece_type_val == 1: #queen
                list[9] += 1


    return list


def val_function(board):#return the value of the board for the AI player (black)
    # pawn = 1, knight = 3, bishop = 3, rook = 5, queen = 9
    # black =* 1, white =* -1
    val = 0
    piece_count = get_piece_count(board)
    f1, w1 = piece_count[0], -1
    f2, w2 = piece_count[1], -3
    f3, w3 = piece_count[2], -3
    f4, w4 = piece_count[3], -5
    f5, w5 = piece_count[4], -9
    f6, w6 = piece_count[5], 1
    f7, w7 =piece_count[6], 3
    f8, w8 = piece_count[7], 3
    f9, w9 = piece_count[8], 5
    f10, w10 = piece_count[9], 9
    f11, w11 = 1 if board.is_it_checkmate(Color.WHITE) else 0, 1000000
    f12, w12 = -1 if board.is_it_checkmate(Color.BLACK) else 0, 1000000

    val = f1*w1 + f2*w2 + f3*w3 + f4*w4 + f5*w5 + f6*w6 + f7*w7 + f8*w8 + f9*w9 + f10*w10 + f11*w11 + f12*w12





    return val
# B=black, W=white, P=pawn, N=knight, B=bishop, R=rook, Q=queen, K=king
# return piece count for each type of piece

# minmax algorithm , alpha beta pruning
def minmax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        return val_function(board)
    if maximizingPlayer: #ai player (black)
        max_eval = -1000000
        for move in board.get_all_moves(Color.BLACK):

            child = board.creat_child_bord(move)
            eval = minmax(child, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else: #opponent player (white)
        min_eval = 1000000
        for move in board.get_all_moves(Color.WHITE):
            child = board.creat_child_bord(move)
            eval = minmax(child, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval