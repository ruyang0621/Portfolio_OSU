# Author: Ru Yang
# Last Modified: 04/01/2021
# Descirption: This file contains a class to represent the board of Janggi game.

import pygame
from .constants import JANGGI_BOARD, OFFSET
from .ChessPiece import *

class Board:
    """Represents a board of Janggi Game."""

    def __init__(self):
        """Creates a board for Janggi Game."""
        self._board = [
            [Chariot("red"), Elephant("red"), Horse("red"), Guard("red"), 'E', Guard("red"), Elephant("red"), Horse("red"), Chariot("red")],
            ['E', 'E', 'E', 'E', General("red"), 'E', 'E', 'E', 'E'], 
            ['E', Cannon("red"), 'E', 'E', 'E', 'E', 'E', Cannon("red"), 'E'],
            [Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red")],
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            [Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue")],
            ['E', Cannon("blue"), 'E', 'E', 'E', 'E', 'E', Cannon("blue"), 'E'],
            ['E', 'E', 'E', 'E', General("blue"), 'E', 'E', 'E', 'E'], 
            [Chariot("blue"), Elephant("blue"), Horse("blue"), Guard("blue"), 'E', Guard("blue"), Elephant("blue"), Horse("blue"), Chariot("blue")]
        ]
        self._red_fortress = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
        self._blue_fortress = [[7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5]]
        self._red_spec_pos = [[0, 4], [1, 3], [1, 5], [2, 4]]
        self._blue_spec_pos = [[7, 4], [8, 3], [8, 5], [9, 4]]

    
    def draw_board(self, win):
        """Draws a Janggi board on the window."""
        win.blit(JANGGI_BOARD, (0, OFFSET))
        for index_1, piece_row in enumerate(self._board):
            for index_2, piece in enumerate(piece_row):
                if piece != 'E':
                    piece.draw_piece(win, [index_1, index_2])


    def get_board(self):
        """Returns the board object."""
        return self._board
    

    def set_board(self, pos, piece):
        """
        Takes as parameters a list contains position coord and a chess piece 
        object (or 'E'). Then update the chess piece on this position. 
        """
        self._board[pos[0]][pos[1]] = piece
    

    def get_checker(self, pos):
        """
        Takes as a parameter a list contains start coord and end coord
        Returns which object is on the specific checker.
        """
        return self._board[pos[0]][pos[1]]

    
    def get_general_pos(self, color_string):
        """Takes the color of the player and returns the genral position."""
        for index_1, board_row in enumerate(self._board):
            for index_2, piece in enumerate(board_row):
                if piece != 'E' and piece.get_chess_piece_type() == "General":
                    if piece.get_color() == color_string:
                        return [index_1, index_2]

    
    def get_red_fortress(self):
        """Returns a list that contains the locations of red fortress."""
        return self._red_fortress
    

    def get_blue_fortress(self):
        """Returns a list that contains the locations of blue fortress."""
        return self._blue_fortress

    
    def get_red_spec_pos(self):
        """Returns the list that contains four special locations in the red fortress."""
        return self._red_spec_pos
    
    
    def get_blue_spec_pos(self):
        """Returns the list that contains four special locations in the blue fortress."""
        return self._blue_spec_pos
