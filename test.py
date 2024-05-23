import chess_ai


play_with_computer = False
# Initialize a new board state
board = chess_ai.PyBoardState()

# Move a piece
board.move_piece((1, 4), (3, 4))  # Move black pawn from e7 to e5

# Get all possible moves for white
moves = board.get_all_moves(0)
print(moves)

x = board.get_board_as_string()
print(len(x))

def map_char_to_symbol(char):
    if char == 'P':
        return '♙'
    elif char == 'R':
        return '♖'
    elif char == 'N':
        return '♘'
    elif char == 'B':
        return '♗'
    elif char == 'Q':
        return '♕'
    elif char == 'K':
        return '♔'
    elif char == 'p':
        return '♟'
    elif char == 'r':
        return '♜'
    elif char == 'n':
        return '♞'
    elif char == 'b':
        return '♝'
    elif char == 'q':
        return '♛'
    elif char == 'k':
        return '♚'
    
    return ''

def str_to_list(str):
    list = [['' for i in range(8)] for j in range(8)]
    row = 0
    col = 0
    for i in range(len(str)):
        if str[i] == '\n':
            row += 1
            col = 0
        else:
            list[row][col] = str[i]
            col += 1
    return list
print(str_to_list(x))




from enum import Enum
import random
import tkinter as tk
from tkinter import messagebox
import copy
import ai
### gui
class ChessGUI:
    def __init__(self, root, board_state):
        self.root = root
        self.board_state = board_state
        self.board_list = str_to_list(self.board_state.get_board_as_string())
        self.selected_piece = None
        self.buttons = {}
        self.create_chess_board()
        
    def selected_pice_is_valid(self, position):
        selected_is_white = self.board_list[position[0]][position[1]].isupper()
        turn_is_white = self.board_state.get_turn() == 0
        return selected_is_white == turn_is_white
    
    def is_valid_move(self, move):
        return move in self.board_state.get_move_for_location(move[0])
    
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
            self.buttons[pos].config(text=' ', bg='dark khaki' if (pos[0] + pos[1]) % 2 == 0 else 'dark green')
            # Update all buttons with current pieces, changing the text color based on the piece color

            # Update all buttons with current pieces, changing the text color based on the piece color
            for i in range(8):
                for j in range(8):
                    char = self.board_list[i][j]
                    if char != '':
                        symbol = map_char_to_symbol(char)
                        text_color = 'black' if char.islower() else 'white'
                        self.buttons[(i, j)].config(text=symbol, foreground=text_color)

            

    def on_click(self, pos):
        if not self.selected_piece:
            if self.board_list[pos[0]][pos[1]] != '.':
                self.selected_piece = pos
                self.buttons[pos].config(bg='blue')
            else:
                messagebox.showinfo("Invalid", "No piece at this position!")
        else:
            move = (self.selected_piece, pos)
            #if self.board_state.selcted_pice_is_valid(self.selected_piece) and self.board_state.is_valid_move(move):
            if self.selected_pice_is_valid(self.selected_piece) and self.is_valid_move(move):    
                self.board_state.move_piece(move[0], move[1])
                self.board_list = str_to_list(self.board_state.get_board_as_string())
                self.update_board()
                self.buttons[self.selected_piece].config(bg='white' if (self.selected_piece[0] + self.selected_piece[1]) % 2 == 0 else 'gray')
                self.selected_piece = None
                if self.board_state.get_turn() == 1 and play_with_computer:
                    self.make_computer_move()

                    self.update_board()
                    #todo: check if the game is over
                    '''
                    if self.board_state.is_it_checkmate(Color.WHITE):
                        messagebox.showinfo("Game Over", "You lose!")
                        self.root.quit()
                    '''
            else:
                messagebox.showinfo("Invalid", "Invalid move!")
                self.buttons[self.selected_piece].config(bg='white' if (self.selected_piece[0] + self.selected_piece[1]) % 2 == 0 else 'gray')
                self.selected_piece = None

    def make_computer_move(self):
        move = ai.chose_move(self.board_state)
        if move is not None:
            #move = random.choice(moves)
            self.board_state.move_piece(move)
            #mark the move on the board
            self.buttons[move[0]].config(bg='blue')
            self.buttons[move[1]].config(bg='blue')
            self.root.update()






        else:
            messagebox.showinfo("Game Over", "You win!")
            self.root.quit()
        self.update_board()


def main():
    root = tk.Tk()
    root.title("Chess Game")

    # Initialize the board state
    bord = chess_ai.PyBoardState()

    # Create GUI
    gui = ChessGUI(root, bord)

    root.mainloop()

if __name__ == "__main__":
    # add comend line arguments

    main()