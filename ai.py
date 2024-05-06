import random
import noUI

def chose_move(board):
    moves = []
    for location in board.black_locations:
        moves += board.get_move_for_location(location)
    move = random.choice(moves) if moves !=[] else None

    return move

def val_function(board):#return the value of the board
    sum=0
    for key,val in board.pieces:
        if val.PiceType== noUI.Piece_type.Q:
            if val.color==noUI.Color.BLACK:
                sum+=9
            else:
                sum-=9
        elif val.PiceType== noUI.Piece_type.R:
            if val.color==noUI.Color.BLACK:
                sum+=5
            else:
                sum-=5
        elif val.PiceType== noUI.Piece_type.B:
            if val.color==noUI.Color.BLACK:
                sum+=3
            else:
                sum-=3
        elif val.PiceType== noUI.Piece_type.N:
            if val.color==noUI.Color.BLACK:
                sum+=3
            else:
                sum-=3
        elif val.PiceType== noUI.Piece_type.P:
            if val.color==noUI.Color.BLACK:
                sum+=1
            else:
                sum-=1

    return sum


