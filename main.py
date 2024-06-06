import chess_ai
import time
from enum import Enum
import random
import tkinter as tk
from tkinter import messagebox
import copy

# test argument
play_with_computer = True
# Initialize a new board state
board = chess_ai.PyBoardState()

# map the char to the unicode symbol
# argument: char
# return: unicode symbol
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

# transform the string representation of the board to a 2D list
# argument: str
# return: list
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



# GUI class, create the chess board and handle the user input
class ChessGUI:
    def __init__(self, root, board_state):
        self.root = root
        self.board_state = board_state
        self.board_list = str_to_list(self.board_state.get_board_as_string())
        self.selected_piece = None
        self.buttons = {}
        self.create_chess_board()

    # check if the selected piece is valid    
    def selected_pice_is_valid(self, position):
        selected_is_white = self.board_list[position[0]][position[1]].isupper()
        turn_is_white = self.board_state.get_turn() == 0
        return selected_is_white == turn_is_white
    
    # check if the move is valid
    def is_valid_move(self, move):
        return move in self.board_state.get_move_for_location(move[0])
    
    # create the chess board
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

    # Update the board with the current pieces
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

            
    # Handle the user click event
    def on_click(self, pos):
        if not self.selected_piece:
            if self.board_list[pos[0]][pos[1]] != '.':
                self.selected_piece = pos
                self.buttons[pos].config(bg='blue')
            else:
                messagebox.showinfo("Invalid", "No piece at this position!")
        else:
            move = (self.selected_piece, pos)
            if self.selected_pice_is_valid(self.selected_piece) and self.is_valid_move(move):    
                self.board_state.move_piece(move[0], move[1])
                self.board_list = str_to_list(self.board_state.get_board_as_string())
                self.update_board()
                self.buttons[self.selected_piece].config(bg='white' if (self.selected_piece[0] + self.selected_piece[1]) % 2 == 0 else 'gray')
                self.selected_piece = None
                if self.board_state.get_turn() == 1 and play_with_computer:
                    self.make_computer_move()
                    self.board_list = str_to_list(self.board_state.get_board_as_string())
                    self.update_board()
                    
                    
                    if self.board_state.get_all_moves(0) == []:
                        if self.board_state.is_king_in_check(0):
                            messagebox.showinfo("Game Over", "You loss!")
                        else:
                            messagebox.showinfo("Game Over", "Draw!")
                        
            else:
                messagebox.showinfo("Invalid", "Invalid move!")
                self.buttons[self.selected_piece].config(bg='white' if (self.selected_piece[0] + self.selected_piece[1]) % 2 == 0 else 'gray')
                self.selected_piece = None

    # Make the computer move
    def make_computer_move(self):
        move = self.board_state.get_best_move()
        if move is not None:
            
            self.board_state.move_piece(move[0], move[1])
            #mark the move on the board
            self.buttons[move[0]].config(bg='blue')
            self.buttons[move[1]].config(bg='blue')
            self.root.update()

        #No move available, game over
        else:
            #check if the king is in check, means checkmate
            if self.board_state.is_king_in_check(1):
                messagebox.showinfo("Game Over", "You win!")
            #no move available and king is not in check, means draw
            else:
                messagebox.showinfo("Game Over", "Draw!")

            
        

def main():
    root = tk.Tk()
    root.title("Chess Game")

    # Initialize the board state
    board = chess_ai.PyBoardState()

    # Create GUI
    gui = ChessGUI(root, board)

    root.mainloop()

if __name__ == "__main__":
  

    main()