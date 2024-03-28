# Importing Modules
import copy

import pygame
from enum import Enum
import ast

# Initialising pygame module
pygame.init()

# Setting Width and height of the Chess Game screen
WIDTH = 800
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Chess Game')

font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 60
"""black_king_location = (400, 700)
white_king_location = (400, 0)"""

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
selection = 100


def tupule_string_to_int(tupule_string):
    return ast.literal_eval(tupule_string)


def tupule_int_to_string(tupule_int):
    return f'{tupule_int[0], tupule_int[1]}'


# a class for the chess pieces
class Piece_type(Enum):
    QUEEN = 1
    KING = 2
    ROOK = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN = 6


# todo : refactor this function

def not_color(color):
    if color == 'white':
        return 'black'
    else:
        return 'white'


class ChessPiece:
    def __init__(self, image, color, position, type: Piece_type):
        self.image = image
        self.color = color
        self.position = position
        self.Piece_type = type
        self.move_count = 0
        self.move_options = []

    def draw(self):
        screen.blit(self.image, self.position)


# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))

black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))

black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))

black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))

black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))

black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))

white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))

white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))

white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))

white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))

white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))

white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))

# chess pieces and starting position dictionary
white_pieces = {'(300, 0)': ChessPiece(white_queen, 'white', (300, 0), Piece_type.QUEEN),
                '(400, 0)': ChessPiece(white_king, 'white', (400, 0), Piece_type.KING),
                '(0, 0)': ChessPiece(white_rook, 'white', (0, 0), Piece_type.ROOK),
                '(700, 0)': ChessPiece(white_rook, 'white', (700, 0), Piece_type.ROOK),
                '(100, 0)': ChessPiece(white_knight, 'white', (100, 0), Piece_type.KNIGHT),
                '(600, 0)': ChessPiece(white_knight, 'white', (600, 0), Piece_type.KNIGHT),
                '(200, 0)': ChessPiece(white_bishop, 'white', (200, 0), Piece_type.BISHOP),
                '(500, 0)': ChessPiece(white_bishop, 'white', (500, 0), Piece_type.BISHOP),
                '(0, 100)': ChessPiece(white_pawn, 'white', (0, 100), Piece_type.PAWN),
                '(100, 100)': ChessPiece(white_pawn, 'white', (100, 100), Piece_type.PAWN),
                '(200, 100)': ChessPiece(white_pawn, 'white', (200, 100), Piece_type.PAWN),
                '(300, 100)': ChessPiece(white_pawn, 'white', (300, 100), Piece_type.PAWN),
                '(400, 100)': ChessPiece(white_pawn, 'white', (400, 100), Piece_type.PAWN),
                '(500, 100)': ChessPiece(white_pawn, 'white', (500, 100), Piece_type.PAWN),
                '(600, 100)': ChessPiece(white_pawn, 'white', (600, 100), Piece_type.PAWN),
                '(700, 100)': ChessPiece(white_pawn, 'white', (700, 100), Piece_type.PAWN)}
white_locations = [tupule_string_to_int(x) for x in white_pieces.keys()]
black_pieces = {'(300, 700)': ChessPiece(black_queen, 'black', (300, 700), Piece_type.QUEEN),
                '(400, 700)': ChessPiece(black_king, 'black', (400, 700), Piece_type.KING),
                '(0, 700)': ChessPiece(black_rook, 'black', (0, 700), Piece_type.ROOK),
                '(700, 700)': ChessPiece(black_rook, 'black', (700, 700), Piece_type.ROOK),
                '(100, 700)': ChessPiece(black_knight, 'black', (100, 700), Piece_type.KNIGHT),
                '(600, 700)': ChessPiece(black_knight, 'black', (600, 700), Piece_type.KNIGHT),
                '(200, 700)': ChessPiece(black_bishop, 'black', (200, 700), Piece_type.BISHOP),
                '(500, 700)': ChessPiece(black_bishop, 'black', (500, 700), Piece_type.BISHOP),
                '(0, 600)': ChessPiece(black_pawn, 'black', (0, 600), Piece_type.PAWN),
                '(100, 600)': ChessPiece(black_pawn, 'black', (100, 600), Piece_type.PAWN),
                '(200, 600)': ChessPiece(black_pawn, 'black', (200, 600), Piece_type.PAWN),
                '(300, 600)': ChessPiece(black_pawn, 'black', (300, 600), Piece_type.PAWN),
                '(400, 600)': ChessPiece(black_pawn, 'black', (400, 600), Piece_type.PAWN),
                '(500, 600)': ChessPiece(black_pawn, 'black', (500, 600), Piece_type.PAWN),
                '(600, 600)': ChessPiece(black_pawn, 'black', (600, 600), Piece_type.PAWN),
                '(700, 600)': ChessPiece(black_pawn, 'black', (700, 600), Piece_type.PAWN)}
black_locations = [tupule_string_to_int(x) for x in black_pieces.keys()]


class bord_state:
    def __init__(self, white_pieces, black_pieces, white_locations, black_locations, turn_step):
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.white_locations = white_locations
        self.black_locations = black_locations
        self.turn_step = turn_step
        if turn_step <= 1:
            self.white_king_location = (400, 0)
            self.black_king_location = (400, 700)

    def __copy__(self):
        return bord_state(self.white_pieces, self.black_pieces, self.white_locations, self.black_locations,
                          self.turn_step)

    def __deepcopy__(self, memodict={}):
        return bord_state(copy.deepcopy(self.white_pieces), copy.deepcopy(self.black_pieces),
                          copy.deepcopy(self.white_locations), copy.deepcopy(self.black_locations), self.turn_step)

    def update_pieces_moves(self):
        '''for piece in self.white_pieces.values():
            piece.move_options_update(False)
        for piece in self.white_pieces.black_pieces.values():
            piece.move_options_update(False)'''
        for piece in self.white_pieces.values():
            piece.move_options = self.get_move_options(piece, False)
        for piece in self.black_pieces.values():
            piece.move_options = self.get_move_options(piece, False)

    def move(self, piece, new_position):
        piece.position = new_position
        piece.move_count += 1
        #piece.move_options_update()
        bord.move_options_update(piece)
        self.update_pieces_moves()
        self.turn_step += 1
        if piece.Piece_type == Piece_type.KING:
            if piece.color == 'white':
                self.white_king_location = new_position
            else:
                self.black_king_location = new_position


    def __check_king(self, piece):

        out = []
        if piece.color == 'white':
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations

        # 8 squares to check for kings, they can go one square any direction
        targets = [(100, 0), (100, 100), (100, -100), (-100, 0),
                   (-100, 100), (-100, -100), (0, 100), (0, -100)]
        for i in range(8):
            target = (piece.position[0] + targets[i][0], piece.position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 700 and 0 <= target[1] <= 700:
                out.append(target)
        # todo: add castling

        return out

    def __check_queen(self, piece):

        return self.__check_bishop(piece) + self.__check_rook(piece)

    def __check_bishop(self, piece):

        out = []
        if piece.color == 'white':
            friends_list = self.white_locations
            enemies_list = self.black_locations

        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations

        for i in range(4):  # up-right, up-left, down-right, down-left
            path = True
            chain = 1
            if i == 0:  # up-right
                x, y = 100, -100

            elif i == 1:  # up-left
                x, y = -100, -100

            elif i == 2:  # down-right
                x, y = 100, 100

            else:  # down-left
                x, y = -100, 100

            while path:
                if (piece.position[0] + (chain * x), piece.position[1] + (chain * y)) not in friends_list and \
                        0 <= piece.position[0] + (chain * x) <= 700 and 0 <= piece.position[1] + (
                        chain * y) <= 700:  # in bounds
                    out.append(
                        (piece.position[0] + (chain * x), piece.position[1] + (chain * y)))
                    if (piece.position[0] + (chain * x),
                        piece.position[1] + (chain * y)) in enemies_list:  # enemy piece detected, stop path
                        path = False
                    chain += 1
                else:
                    path = False
        return out

    def __check_knight(self, piece):

        out = []
        if piece.color == 'white':
            friends_list = self.white_locations
            enemies_list = self.black_locations

        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations
        # 8 squares to check for knights, L shape

        targets = [(100, 200), (100, -200), (200, 100), (200, -100),
                   (-100, 200), (-100, -200), (-200, 1000), (-200, -100)]
        for i in range(8):
            target = (piece.position[0] + targets[i][0], piece.position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 700 and 0 <= target[1] <= 700:
                out.append(target)

        return out

    def __check_rook(self, piece):

        out = []
        if piece.color == 'white':
            friends_list = self.white_locations
            enemies_list = self.black_locations

        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations
        for i in range(4):  # down, up, right, left
            path = True
            chain = 1
            if i == 0:  # down
                x, y = 0, 100
            elif i == 1:  # up
                x, y = 0, -100
            elif i == 2:  # right
                x, y = 100, 0
            else:  # left
                x, y = -100, 0
            while path:
                if (piece.position[0] + (chain * x), piece.position[1] + (chain * y)) not in friends_list and \
                        0 <= piece.position[0] + (chain * x) <= 700 and 0 <= piece.position[1] + (chain * y) <= 700:
                    out.append(
                        (piece.position[0] + (chain * x), piece.position[1] + (chain * y)))
                    if (piece.position[0] + (chain * x), piece.position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return out

    def __check_pawn(self, piece):

        out = []
        if piece.color == 'white':
            friends_list = self.white_locations
            enemies_list = self.black_locations

            one_down = (piece.position[0], piece.position[1] + 100)
            two_down = (piece.position[0], piece.position[1] + 200)
            one_diag_right = (piece.position[0] + 100, piece.position[1] + 100)
            one_diag_left = (piece.position[0] - 100, piece.position[1] + 100)
            if one_down not in friends_list and one_down not in enemies_list and 0 <= one_down[1] <= 700:
                out.append(one_down)
                if piece.move_count == 0 and two_down not in friends_list and two_down not in enemies_list:
                    out.append(two_down)
            if one_diag_right in enemies_list:
                out.append(one_diag_right)
            if one_diag_left in enemies_list:
                out.append(one_diag_left)
        else:

            friends_list = self.black_locations
            enemies_list = self.white_locations

            one_up = (piece.position[0], piece.position[1] - 100)
            two_up = (piece.position[0], piece.position[1] - 200)
            one_diag_right = (piece.position[0] + 100, piece.position[1] - 100)
            one_diag_left = (piece.position[0] - 100, piece.position[1] - 100)
            if one_up not in enemies_list and one_up not in friends_list and 0 <= one_up[1] <= 700:
                out.append(one_up)
                if piece.move_count == 0 and two_up not in enemies_list and two_up not in friends_list:
                    out.append(two_up)
            if one_diag_right in enemies_list:
                out.append(one_diag_right)
            if one_diag_left in enemies_list:
                out.append(one_diag_left)

        return out

    def get_move_options(self, piece, check_for_bad_moves=True):

        if piece.Piece_type == Piece_type.PAWN:
            #out = piece.__check_pawn()
            out = self.__check_pawn(piece)
        if piece.Piece_type == Piece_type.ROOK:
            out = self.__check_rook(piece)
        if piece.Piece_type == Piece_type.KNIGHT:
            out = self.__check_knight(piece)
        if piece.Piece_type == Piece_type.BISHOP:
            out = self.__check_bishop(piece)
        if piece.Piece_type == Piece_type.QUEEN:
            out = self.__check_queen(piece)

        if piece.Piece_type == Piece_type.KING:
            out = self.__check_king(piece)

        if check_for_bad_moves:
            bad_moves = check_if_move_puts_king_in_check(piece, out)
            for possible_move in bad_moves:
                out.remove(possible_move)

        return out

    def move_options_update(self, piece, check_for_bad_moves=True):
        piece.move_options = self.get_move_options(piece, check_for_bad_moves)
        #piece.get_move_options(check_for_bad_moves)
        return piece.move_options
    def is_there_a_check_on(self, color):
        if color == 'white':
            for piece in self.black_pieces.values():
                if self.white_king_location in piece.move_options:
                    return True
        else:
            for piece in self.white_pieces.values():
                if self.black_king_location in piece.move_options:
                    return True
        return False


bord = bord_state(white_pieces, black_pieces, white_locations, black_locations, 0)


# to do: change the locations of the pieces to a copy of the list
def check_if_move_puts_king_in_check(piece, move_list):
    out = []
    return out
    if piece.color == 'white':
        white_locations_dup = copy.deepcopy(white_locations)
        white_locations_dup.remove(piece.position)

        for move in move_list:

            # check if move puts white king in check
            for piece in black_pieces.values():
                # disregard all the pieces that are pawns , knights, and kings they can't put the king in check from opponent move
                if piece.Piece_type == Piece_type.KING or piece.Piece_type == Piece_type.KNIGHT or piece.Piece_type == Piece_type.PAWN:
                    continue
                # change the position of the piece to the new position
                white_locations_dup.append(move)

                if white_king_location in piece.get_move_options(False, white_locations_dup, None):
                    out.append(move)
                # change the position of the piece back to the original position

                white_locations_dup.remove(move)









    else:
        black_locations_dup = copy.deepcopy(black_locations)
        black_locations_dup.remove(piece.position)

    return out


# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False


# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [
                600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [
                700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(
            status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))


# draw pieces onto board
def draw_pieces(bord):
    for piece in bord.white_pieces.values():
        piece.draw()
    for piece in bord.black_pieces.values():
        piece.draw()


# todo: refactor this function
"""def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(100, 0), (100, 100), (100, -100), (-100, 0),
               (-100, 100), (-100, -100), (0, 100), (0, -100)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 700 and 0 <= target[1] <= 700:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options"""

run = True
turn_counter = 0
print(white_locations)
bord.update_pieces_moves()
print(white_pieces['(400, 100)'].move_options)
print(black_pieces['(400, 600)'].move_options)

while run:
    timer.tick(fps)
    # turn_counter += 1
    screen.fill('dark gray')
    draw_board()
    draw_pieces(bord)





    # pygame.display.flip()

    # check valid moves for selected piece and draw them
    # if selection < 100:
    for move in valid_moves:
        move = (move[0] + 50, move[1] + 50)
        pygame.draw.circle(screen, 'red', move, 10)
        # pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100 * 100
            y_coord = event.pos[1] // 100 * 100
            click_coords = (x_coord, y_coord)
            click_coords_string = tupule_int_to_string(click_coords)
            if turn_step <= 1:  # white turn
                """if click_coords == (8, 8) or click_coords == (9, 8): 
                    winner = 'black'"""
                # selct a piece to move, and draw valid moves
                if click_coords_string in bord.white_pieces:
                    piece_key = click_coords_string
                    valid_moves = bord.move_options_update(bord.white_pieces[click_coords_string])
                    #valid_moves = bord.white_pieces[click_coords_string].move_options_update()
                    if turn_step == 0:  # no piece selected
                        turn_step = 1
                if click_coords in valid_moves:
                    # move the piece

                    #white_pieces[piece_key].move(click_coords)
                    bord.move(bord.white_pieces[piece_key],click_coords)
                    #white_locations.remove(tupule_string_to_int(piece_key))
                    bord.white_locations.remove(tupule_string_to_int(piece_key))
                    #white_locations.append(click_coords)
                    bord.white_locations.append(click_coords)

                    # update the dictionary
                    val = bord.white_pieces.pop(piece_key)
                    bord.white_pieces[tupule_int_to_string(click_coords)] = val
                    # check for captured pieces
                    if click_coords in bord.black_locations:
                        bord.black_locations.remove(click_coords)
                        bord.black_pieces.pop(tupule_int_to_string(click_coords))

                    bord.update_pieces_moves()

                    if bord.is_there_a_check_on('black'):
                        pygame.draw.circle(screen, 'dark red',
                                           (bord.black_king_location[0] + 50, bord.black_king_location[1] + 50), 50,
                                           5)

                    turn_step = 2
                    selection = 100
                    valid_moves = []

                    # pygame.display.flip()

            elif turn_step >= 2:  # black turn
                """if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'"""
                if click_coords_string in bord.black_pieces:
                    piece_key = click_coords_string
                    valid_moves = bord.move_options_update(bord.black_pieces[click_coords_string])
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves:
                    # move the piece
                    #black_pieces[piece_key].move(click_coords)
                    bord.move(bord.black_pieces[piece_key], click_coords)
                    #black_locations.remove(tupule_string_to_int(piece_key))
                    bord.black_locations.remove(tupule_string_to_int(piece_key))
                    #black_locations.append(click_coords)
                    bord.black_locations.append(click_coords)

                    # update the dictionary
                    val = bord.black_pieces.pop(piece_key)
                    bord.black_pieces[tupule_int_to_string(click_coords)] = val



                    # check for captured pieces
                    if click_coords in bord.white_locations:
                        bord.white_locations.remove(click_coords)
                        bord.white_pieces.pop(tupule_int_to_string(click_coords))

                    bord.update_pieces_moves()

                    if bord.is_there_a_check_on('white'):
                        pygame.draw.circle(screen, 'dark red',
                                           (bord.white_king_location[0] + 50, bord.white_king_location[1] + 50), 50,
                                           5)

                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    # pygame.display.flip()
    if bord.is_there_a_check_on('white'):
        pygame.draw.circle(screen, 'dark red', (bord.white_king_location[0] + 50, bord.white_king_location[1] + 50), 50,
                           5)
        # pygame.display.flip()

    if bord.is_there_a_check_on('black'):
        pygame.draw.circle(screen, 'dark red', (bord.black_king_location[0] + 50, bord.black_king_location[1] + 50), 50,
                           5)
    pygame.display.flip()
    # if a piece is selected and a valid move is clicked
