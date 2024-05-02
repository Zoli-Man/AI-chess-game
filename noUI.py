from enum import Enum
import random
import tkinter as tk
from tkinter import messagebox
import copy

class Piece_type(Enum):
    Q = 1
    K = 2
    R = 3
    B = 4
    N = 5
    P = 6


class Color(Enum):
    WHITE = 1
    BLACK = 2

class ChessPiece:
    def __init__(self, piece_type, color,position):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.move_count = 0
        #self.move_options = []

    def move(self, new_position):
        # make sure the move is valid
        self.position = new_position
        self.move_count += 1



    def __str__(self):
        # example: '♔' for white king, '♚' for black king
        if self.color == Color.WHITE:
            if self.piece_type == Piece_type.Q:
                return '♕'
            elif self.piece_type == Piece_type.K:
                return '♔'
            elif self.piece_type == Piece_type.R:
                return '♖'
            elif self.piece_type == Piece_type.B:
                return '♗'
            elif self.piece_type == Piece_type.N:
                return '♘'
            elif self.piece_type == Piece_type.P:
                return '♙'
        else:
            if self.piece_type == Piece_type.Q:
                return '♛'
            elif self.piece_type == Piece_type.K:
                return '♚'
            elif self.piece_type == Piece_type.R:
                return '♜'
            elif self.piece_type == Piece_type.B:
                return '♝'
            elif self.piece_type == Piece_type.N:
                return '♞'
            elif self.piece_type == Piece_type.P:
                return '♟'

class BordState:
    def __init__(self,new_bord = True, dic = None, turn = None, move_count = None):
        if new_bord:
            #make self.pices a dictionary with key as position and value as piece
            self.pieces = {}
            self.turn = Color.WHITE
            self.move_count = 0
            #initialize the board with pieces
            self.pieces[(0, 0)] = ChessPiece(Piece_type.R, Color.WHITE, (0, 0))
            self.pieces[(0, 1)] = ChessPiece(Piece_type.N, Color.WHITE, (0, 1))
            self.pieces[(0, 2)] = ChessPiece(Piece_type.B, Color.WHITE, (0, 2))
            self.pieces[(0, 3)] = ChessPiece(Piece_type.Q, Color.WHITE, (0, 3))
            self.pieces[(0, 4)] = ChessPiece(Piece_type.K, Color.WHITE, (0, 4))
            self.pieces[(0, 5)] = ChessPiece(Piece_type.B, Color.WHITE, (0, 5))
            self.pieces[(0, 6)] = ChessPiece(Piece_type.N, Color.WHITE, (0, 6))
            self.pieces[(0, 7)] = ChessPiece(Piece_type.R, Color.WHITE, (0, 7))
            for i in range(8):
                self.pieces[(1, i)] = ChessPiece(Piece_type.P, Color.WHITE, (1, i))
                self.pieces[(6, i)] = ChessPiece(Piece_type.P, Color.BLACK, (6, i))
            self.pieces[(7, 0)] = ChessPiece(Piece_type.R, Color.BLACK, (7, 0))
            self.pieces[(7, 1)] = ChessPiece(Piece_type.N, Color.BLACK, (7, 1))
            self.pieces[(7, 2)] = ChessPiece(Piece_type.B, Color.BLACK, (7, 2))
            self.pieces[(7, 3)] = ChessPiece(Piece_type.Q, Color.BLACK, (7, 3))
            self.pieces[(7, 4)] = ChessPiece(Piece_type.K, Color.BLACK, (7, 4))
            self.pieces[(7, 5)] = ChessPiece(Piece_type.B, Color.BLACK, (7, 5))
            self.pieces[(7, 6)] = ChessPiece(Piece_type.N, Color.BLACK, (7, 6))
            self.pieces[(7, 7)] = ChessPiece(Piece_type.R, Color.BLACK, (7, 7))

            self.black_locations = [x for x in self.pieces if self.pieces[x].color == Color.BLACK]
            self.white_locations = [x for x in self.pieces if self.pieces[x].color == Color.WHITE]
        else:
            self.pieces = dic
            self.turn = turn
            self.move_count = move_count
            self.black_locations = [x for x in self.pieces if self.pieces[x].color == Color.BLACK]
            self.white_locations = [x for x in self.pieces if self.pieces[x].color == Color.WHITE]



    def get_piece(self, position):
        return self.pieces.get(position)

    def move_piece(self, move):
        # move is a  tuple of two tuples, example ((0, 0), (1, 0))
        # move must be a valid move


        start = move[0]
        x = self.pieces.get(move[0])
        end = move[1]


        try:
            move_is_castling = self.pieces.get(start).piece_type == Piece_type.K and abs(start[1] - end[1]) > 1

        except:
            print(move)
            print(self)
            exit(1)
        piece = self.get_piece(start)
        if move_is_castling:
            # move the rook
            left = end[1] < start[1]
            rook_piece = self.get_piece((start[0], 0 if left else 7))
            rook_piece.move((start[0], 3 if left else 5))
            self.pieces[(start[0], 3 if left else 5)] = rook_piece
            del self.pieces[(start[0], 0 if left else 7)]

        # check if the move is a capture

        is_capture = self.get_piece(end) is not None and self.get_piece(end).color != piece.color

        if piece.color == Color.BLACK:
            self.black_locations.remove(start)
            self.black_locations.append(end)
            if is_capture:
                self.white_locations.remove(end)
        else:
            self.white_locations.remove(start)
            self.white_locations.append(end)
            if is_capture:
                self.black_locations.remove(end)




        # update the locations of the pieces

        piece.move(end)
        self.pieces[end] = piece
        del self.pieces[start]
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        self.move_count += 1







    def creat_child_bord(self, move, check_test = True):
        # move is a  tuple of two tuples, example ((0, 0), (1, 0))
        # move must be a valid move

        new_dic = copy.deepcopy(self.pieces)
        new_turn = self.turn

        new_move_count = self.move_count

        #testimg

        x = self.get_piece(move[0])
        if x is None:
            print('error')
            print(move)
            print(self)
            exit(1)


        ###

        child = BordState(False,new_dic,new_turn,new_move_count)
        child.move_piece(move)

        return child

    def get_king_position(self, color):
        for position, piece in self.pieces.items():
            if piece.piece_type == Piece_type.K and piece.color == color:
                return position


    # get all the possible moves for a piece
    # toco: add en passant
    # todo: add promotion
    # todo: add logic for check and prevent pieces from moving if it puts the king in check

    def get_move_for_location(self, position,check_test = True):
        piece = self.get_piece(position)
        out = []
        if piece is None:
            return out
        piece_type = piece.piece_type

        if piece_type == Piece_type.P:
            out = self.get_pawn_moves(piece)
        elif piece_type == Piece_type.N:
            out = self.get_knight_moves(piece)
        elif piece_type == Piece_type.B:
            out = self.get_bishop_moves(piece)
        elif piece_type == Piece_type.R:
            out = self.get_rook_moves(piece)
        elif piece_type == Piece_type.Q:
            out = self.get_queen_moves(piece)
        elif piece_type == Piece_type.K:
            out = self.get_king_moves(piece)

        # remove moves that put the king in danger
        if check_test:
            enemies_moves = []
            for location in self.black_locations if piece.color == Color.WHITE else self.white_locations:
                enemies_moves += self.get_move_for_location(location,False)  # list of tuples of possible moves for the enemy e.g. [((0, 0), (1, 8)) , ((0, 0), (1, 7)) ...]

            if piece.piece_type == Piece_type.K: # king can't move to a position that is under attack
                for move in out.copy():
                    bad_move = any([move[1] == x[1] for x in enemies_moves])
                    if bad_move:
                        out.remove(move)
            else: #other pieces can't move if it puts the king in danger
                i=0
                print(out)
                for move in out.copy():
                    ###
                    x = self.get_piece(move[0])
                    if x is None:
                        print(piece)
                        print('error 1')
                        print(move)
                        print(piece.piece_type)
                        print(self)
                        print(out)
                        exit(1)
                    ###
                    else:
                        print(f"ok {i}")
                        i+=1

                    child = self.creat_child_bord(move, False)
                    if child.is_check(piece.color):
                        out.remove(move)






        return out



    def get_king_moves(self, piece):
        moves = []
        x, y = piece.position
        color = piece.color
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < 8 and 0 <= y + j < 8:
                    if self.get_piece((x + i, y + j)) is None or self.get_piece((x + i, y + j)).color != color:
                        moves.append(((x, y), (x + i, y + j)))



        # add castling moves
        if piece.move_count == 0:
            if color == Color.BLACK:
                if self.get_piece((7, 1)) is None and self.get_piece((7, 2)) is None and self.get_piece((7, 3)) is None:
                    if self.get_piece((7, 0)) is not None and self.get_piece((7, 0)).move_count == 0:
                        moves.append(((7, 4), (7, 2)))
                if self.get_piece((7, 5)) is None and self.get_piece((7, 6)) is None:
                    if self.get_piece((7, 7)) is not None and self.get_piece((7, 7)).move_count == 0:
                        moves.append(((7, 4), (7, 6)))
            else:
                if self.get_piece((0, 1)) is None and self.get_piece((0, 2)) is None and self.get_piece((0, 3)) is None:
                    if self.get_piece((0, 0)) is not None and self.get_piece((0, 0)).move_count == 0:
                        moves.append(((0, 4), (0, 2)))
                if self.get_piece((0, 5)) is None and self.get_piece((0, 6)) is None:
                    if self.get_piece((0, 7)) is not None and self.get_piece((0, 7)).move_count == 0:
                        moves.append(((0, 4), (0, 6)))
        return moves






    def get_pawn_moves(self, piece):
        moves = []
        x, y = piece.position
        color = piece.color
        direction = 1 if color == Color.WHITE else -1
        if self.get_piece((x + direction, y)) is None:
            moves.append(((x, y), (x + direction, y)))
            if piece.move_count == 0 and self.get_piece((x + 2 * direction, y)) is None:
                moves.append(((x, y), (x + 2 * direction, y)))
        if y > 0 and self.get_piece((x + direction, y - 1)) is not None:
            moves.append(((x, y), (x + direction, y - 1)))
        if y < 7 and self.get_piece((x + direction, y + 1)) is not None:
            moves.append(((x, y), (x + direction, y + 1)))

        return moves

    def get_knight_moves(self, piece):
        moves = []
        x, y = piece.position
        color = piece.color
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3 and 0 <= x + i < 8 and 0 <= y + j < 8:
                    if self.get_piece((x + i, y + j)) is None or self.get_piece((x + i, y + j)).color != color:
                        moves.append(((x, y), (x + i, y + j)))


        return moves

    def get_bishop_moves(self, piece):
        moves = []
        x, y = piece.position
        color = piece.color
        for i in range(4):
            path = True
            chain = 1
            if i ==0: # up right
                a,b = 1, -1
            elif i == 1: # up left
                a,b = -1, -1
            elif i == 2: # down right
                a,b = 1, 1
            else: # down left
                a,b = -1, 1
            while path:
                if 0 <= x + chain*a < 8 and 0 <= y + chain*b < 8:
                    if self.get_piece((x + chain*a, y + chain*b)) is None:
                        moves.append(((x, y), (x + chain*a, y + chain*b)))
                    elif self.get_piece((x + chain*a, y + chain*b)).color != color:
                        moves.append(((x, y), (x + chain*a, y + chain*b)))
                        path = False
                    else:
                        path = False
                else:
                    path = False
                chain += 1
        return moves

    def get_rook_moves(self, piece):
        moves = []
        x, y = piece.position
        color = piece.color
        for i in range(4):
            path = True
            chain = 1
            if i ==0: # up
                a,b = 1, 0
            elif i == 1: # down
                a,b = -1, 0
            elif i == 2: # right
                a,b = 0, 1
            else: # left
                a,b = 0, -1
            while path:
                if 0 <= x + chain*a < 8 and 0 <= y + chain*b < 8:
                    if self.get_piece((x + chain*a, y + chain*b)) is None:
                        moves.append(((x, y), (x + chain*a, y + chain*b)))
                    elif self.get_piece((x + chain*a, y + chain*b)).color != color:
                        moves.append(((x, y), (x + chain*a, y + chain*b)))
                        path = False
                    else:
                        path = False
                else:
                    path = False
                chain += 1
        return moves
    def get_queen_moves(self, piece):
        moves = []
        moves += self.get_bishop_moves(piece)
        moves += self.get_rook_moves(piece)
        return moves

    def is_valid_move(self, move):
        # check if the move is valid
        # check if the move is in the list of possible moves
        return move in self.get_move_for_location(move[0])

    def selcted_pice_is_valid(self, position):
        return self.get_piece(position).color == self.turn

    def is_check(self, color):
        king_position = self.get_king_position(color)
        for position, piece in self.pieces.items():
            if piece.color != color: # check if the piece is of the opposite color
                for move in self.get_move_for_location(position, False):
                    if move[1] == king_position:
                        return True
        return False

    def __str__(self):
        bord = ''
        for i in range(8):
            for j in range(8):
                piece = self.get_piece((i, j))
                if piece is None:
                    bord += '.'
                else:
                    bord += str(piece)
            bord += '\n'
        return bord


### gui
class ChessGUI:
    def __init__(self, root, board_state):
        self.root = root
        self.board_state = board_state
        self.selected_piece = None
        self.buttons = {}
        self.create_chess_board()

    def create_chess_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        # Prevent frame from resizing
        board_frame.pack_propagate(False)

        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                button = tk.Button(board_frame, bg=color, text=' ', font=('Courier', 24, 'bold'), width=4, height=2,command=lambda pos=(i, j): self.on_click(pos))
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons[(i, j)] = button

        self.update_board()

    def update_board(self):
        # Clear all buttons before updating to prevent old piece icons from persisting
        for pos in self.buttons:
            self.buttons[pos].config(text=' ', bg='white' if (pos[0] + pos[1]) % 2 == 0 else 'gray')
            # Update all buttons with current pieces, changing the text color based on the piece color
            for position, piece in self.board_state.pieces.items():
                if piece is not None:
                    symbol = str(piece)
                    text_color = 'red' if piece.color == Color.BLACK else 'black'
                    self.buttons[position].config(text=symbol, foreground=text_color)

    def on_click(self, pos):
        if not self.selected_piece:
            if self.board_state.get_piece(pos):
                self.selected_piece = pos
                self.buttons[pos].config(bg='green')
            else:
                messagebox.showinfo("Invalid", "No piece at this position!")
        else:
            move = (self.selected_piece, pos)
            if self.board_state.selcted_pice_is_valid(self.selected_piece) and self.board_state.is_valid_move(move):
                self.board_state.move_piece(move)
                self.update_board()
                self.buttons[self.selected_piece].config(bg='white' if (self.selected_piece[0] + self.selected_piece[1]) % 2 == 0 else 'gray')
                self.selected_piece = None
                if self.board_state.turn == Color.BLACK:
                    self.make_computer_move()
            else:
                messagebox.showinfo("Invalid", "Invalid move!")
                self.buttons[self.selected_piece].config(bg='white' if (self.selected_piece[0] + self.selected_piece[1]) % 2 == 0 else 'gray')
                self.selected_piece = None

    def make_computer_move(self):
        moves = []
        for location in self.board_state.black_locations:
            moves += self.board_state.get_move_for_location(location)
        if moves:
            move = random.choice(moves)
            self.board_state.move_piece(move)
        self.update_board()


def main():
    root = tk.Tk()
    root.title("Chess Game")

    # Initialize the board state
    bord = BordState()

    # Create GUI
    gui = ChessGUI(root, bord)

    root.mainloop()

if __name__ == "__main__":
    main()



'''
bord = BordState()
print(bord)

game_over = False
while not game_over:
    if bord.turn == Color.WHITE:
        try:
            print('Turn: ', bord.turn)
            move = input('Enter your move: ')
            # make sure the move is in the form a3 a4



            # enter the move in the form a3 a4
            move = move.split(' ')
            move = ((int(move[0][1]) - 1, ord(move[0][0]) - 97), (int(move[1][1]) - 1, ord(move[1][0]) - 97))
            x = bord.is_valid_move(move)
            if bord.selcted_pice_is_valid(move[0]) and bord.is_valid_move(move):
                bord.move_piece(move)
            else:
                print('Invalid move')
                # back to the start of the loop
                continue
        except:
            print('Invalid move')
            # back to the start of the loop
            continue
    else:
        # make the computer move a random move
        print('Turn: ', bord.turn)
        print('Computer move')
        # get all the possible moves
        moves = []
        for location in bord.black_locations:
            moves += bord.get_move_for_location(location)
        move = random.choice(moves)
        bord.move_piece(move)

    print(bord)



'''


