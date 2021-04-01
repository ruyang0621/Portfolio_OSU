# Author: Ru Yang
# Date: 02/28/2021
# Description: This program is designed for playing an abstract board game call Janggi. It has Blue
#              and Red as the competing players and Blue as the starting player. The program does not 
#              implement the rules regarding the perpetual check, position repetition, any kind of draw,
#              or the miscellaneous rules. The game ends when one player checkmates the other's general.


class JanggiGame:
    """Represents a Janggi Game."""

    def __init__(self):
        """Initializes all data members for a round of the JanggiGame."""
        self._game_state = "UNFINISHED"
        self._current_player = "blue"
        self._next_player = "red"
        self._checked = None
        self._alpha_num = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self._chess_board = board()
     
    def get_current_player(self):
        """Returns current player."""
        return self._current_player
    
    def get_checked(self):
        """Returns the player who is in checked."""
        return self._checked

    def get_game_state(self):
        """Returns the state of current round.""" 
        return self._game_state
    
    def get_chess_board(self):
        """Returns the current chess board."""
        return self._chess_board

    def is_in_check(self, player):
        """Checks if the input player is in check."""
        if self._checked == player:
            return True
        return False
    
    def general_check_state(self, general_pos, opponent_player):
        """Checks if the input genral is checked by opponent."""
        for index_1, board_row in enumerate(self._chess_board.get_board()):
            for index_2, piece in enumerate(board_row):
                if piece != 'E':
                    if piece.get_color() == opponent_player:
                        if piece.verify_move([index_1, index_2], general_pos, self._chess_board) == True:
                            return True
        return False

    def convert_char_to_num(self, pos_string):
        """
        Takes a position string as parameters. Returns a list contains 2 numbers 
        that represent the actual row and column on the abstract board.
        """
        return [int(pos_string[1:]) - 1, self._alpha_num[pos_string[0]]]
    
    def checkmate_state(self, next_player):
        """Check if opponent cannot remove current check."""
        for index_1, piece_row in enumerate(self._chess_board.get_board()):
            for index_2, piece in enumerate(piece_row):
                if piece != 'E':
                    if piece.get_color() == next_player:
                        possible_locations = piece.find_move_locations([index_1, index_2], self._chess_board)
                        for location in possible_locations:
                            if location != [index_1, index_2]:
                                location_piece = self._chess_board.get_checker(location)
                                self._chess_board.set_board(location, piece)
                                self._chess_board.set_board([index_1, index_2], 'E')
                                next_general_pos = self._chess_board.get_general_pos(self._next_player)
                                if self.general_check_state(next_general_pos, self._current_player) == False:
                                    self._chess_board.set_board([index_1, index_2], piece)
                                    self._chess_board.set_board(location, location_piece)
                                    return False
                                else:
                                    self._chess_board.set_board([index_1, index_2], piece)
                                    self._chess_board.set_board(location, location_piece)
        return True

    def make_move(self, from_pos, to_pos):
        """
        Takes as two parameters strings that represent the square to move from and square to move to.
        If the movement is valid, make the changes accordingly and return True, else return false.
        """
        print("Attempting: ", from_pos, "->", to_pos)
        # Checks if this round has finished.
        if self._game_state != "UNFINISHED":
            return False

        # Checks if the from_pos is valid.
        start_pos = self.convert_char_to_num(from_pos)
        start_piece = self._chess_board.get_checker(start_pos)
        if start_piece == 'E':
            return False 
        if start_piece.get_color() != self._current_player:
            return False

        # Checks if the player wants to pass.
        if from_pos == to_pos and self._checked != None:
            return False
        if from_pos == to_pos:
            temp = self._current_player
            self._current_player = self._next_player
            self._next_player = temp
            return True      
        
        # Checks if the to_pos is valid.
        end_pos = self.convert_char_to_num(to_pos)
        end_piece = self._chess_board.get_checker(end_pos)
        if end_piece != 'E':
            if end_piece.get_color() == self._current_player:
                return False

        # Checks if the piece can move from start position to end according to the rules.
        result = start_piece.verify_move(start_pos, end_pos, self._chess_board)        
        if result is False:
            return False
        
        self._chess_board.set_board(end_pos, start_piece)
        self._chess_board.set_board(start_pos, 'E')

        # Checks if current move will cause check on current player.
        curr_general_pos = self._chess_board.get_general_pos(self._current_player)
        if self.general_check_state(curr_general_pos, self._next_player) == True:
            self._chess_board.set_board(start_pos, start_piece)
            self._chess_board.set_board(end_pos, end_piece)
            return False
        else:
            if self._checked != None:        # If current player needs remove check.
                self._checked = None
        
        # Checks if current move will cause check on next player.
        next_general_pos = self._chess_board.get_general_pos(self._next_player)
        if self.general_check_state(next_general_pos, self._current_player) == True:
            self._checked = self._next_player

            # opponet general cannot move to remove check
            if self.checkmate_state(self._next_player) == True:
                self._game_state = self._current_player.upper() + "_WON"

        # Switches players.  
        temp = self._current_player
        self._current_player = self._next_player
        self._next_player = temp
        return True   
       

class board:
    """Represents a board of Janggi Game."""

    def __init__(self):
        """Creates a board for Janggi Game."""
        self._board = [[Chariot("red"), Elephant("red"), Horse("red"), Guard("red"), 'E', Guard("red"), Elephant("red"), Horse("red"), Chariot("red")],
                       ['E', 'E', 'E', 'E', General("red"), 'E', 'E', 'E', 'E'], 
                       ['E', Cannon("red"), 'E', 'E', 'E', 'E', 'E', Cannon("red"), 'E'],
                       [Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red"), 'E', Soldier("red")],
                       ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
                       [Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue"), 'E', Soldier("blue")],
                       ['E', Cannon("blue"), 'E', 'E', 'E', 'E', 'E', Cannon("blue"), 'E'],
                       ['E', 'E', 'E', 'E', General("blue"), 'E', 'E', 'E', 'E'], 
                       [Chariot("blue"), Elephant("blue"), Horse("blue"), Guard("blue"), 'E', Guard("blue"), Elephant("blue"), Horse("blue"), Chariot("blue")]]

        self._red_fortress = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
        self._red_spec_pos = [[0, 4], [1, 3], [1, 5], [2, 4]]
        self._blue_fortress = [[7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5]]
        self._blue_spec_pos = [[7, 4], [8, 3], [8, 5], [9, 4]]
    
    def get_board(self):
        """Returns the board object."""
        return self._board
    
    def set_board(self, pos, piece):
        """
        Takes as parameters a list contain start coord and end coord and a chess piece 
        object (or 'E') for an update. Then updates the board.
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


class ChessPiece:
    """Represents a Chess Piece in the JanggiGame."""
    
    def __init__(self, color):
        """Creates a Chess Piece object."""
        self._chess_piece_type = None
        self._color = color
    
    def get_chess_piece_type(self):
        """Returns the type of the Chess Piece."""
        return self._chess_piece_type
    
    def get_color(self):
        """Returns the color of the Chess Piece."""
        return self._color
    
    def find_move_locations(self, piece_pos, current_board):
        """
        Takes the piece position and current board. Returns 
        the possible move locations.
        """
        locations = [piece_pos]
        for index_1, piece_row in enumerate(current_board.get_board()):
            for index_2, piece in enumerate(piece_row):
                if self.verify_move(piece_pos, [index_1, index_2], current_board) == True:
                    if current_board.get_checker([index_1, index_2]) == 'E':
                        locations.append([index_1, index_2])
                    elif current_board.get_checker([index_1, index_2]).get_color() != self._color:
                        locations.append([index_1, index_2]) 
        return locations                 


class General(ChessPiece):
    """Represents a General inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an General object."""
        super().__init__(color)
        self._chess_piece_type = "General"
    
    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists contain (start coord and end coord) and current board object. Checks if 
        the General can move from the start position to the end according to the movement rules of the General.
        """
        if start_pos == end_pos:    # Does not make move.
            return True

        if end_pos not in current_board.get_blue_fortress() and end_pos not in current_board.get_red_fortress():
            return False
        if abs(end_pos[0] - start_pos[0]) not in [0, 1]:
            return False
        if abs(end_pos[1] - start_pos[1]) not in [0, 1]: 
            return False

        if self._color == "blue":
            if start_pos in current_board.get_blue_spec_pos() and end_pos in current_board.get_blue_spec_pos():
                return False
        if self._color == "red":
            if start_pos in current_board.get_red_spec_pos() and end_pos in current_board.get_red_spec_pos():
                return False
        return True


class Guard(ChessPiece):
    """Represents a Guard inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an Guard object."""
        super().__init__(color)
        self._chess_piece_type = "Guard"

    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists contain (start coord and end coord) and current board object. Checks if 
        the Guard can move from the start position to the end according to the movement rules of the Guard.
        """
        if start_pos == end_pos:    # Does not make move.
            return True

        if end_pos not in current_board.get_blue_fortress() and end_pos not in current_board.get_red_fortress():
            return False
        if abs(end_pos[0] - start_pos[0]) not in [0, 1]:
            return False
        if abs(end_pos[1] - start_pos[1]) not in [0, 1]: 
            return False

        if self._color == "blue":
            if start_pos in current_board.get_blue_spec_pos() and end_pos in current_board.get_blue_spec_pos():
                return False
        if self._color == "red":
            if start_pos in current_board.get_red_spec_pos() and end_pos in current_board.get_red_spec_pos():
                return False
        return True


class Chariot(ChessPiece):
    """Represents a Chariot inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an Chariot object."""
        super().__init__(color)
        self._chess_piece_type = "Chariot"

    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists (contain start coord and end coord) and current board object. Checks if 
        the Chariot can move from start position to the end according to the movement rules of the Chariot.
        """

        # If the start_pos and end_pos are not at the same fortress or both not at fortresses, and it is diagonal move return False.
        if start_pos not in current_board.get_blue_fortress() and start_pos not in current_board.get_red_fortress():
            if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                return False
        elif start_pos in current_board.get_blue_fortress(): 
            if end_pos not in current_board.get_blue_fortress():
                if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                    return False
        else:
            if end_pos not in current_board.get_red_fortress():
                if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                    return False

        # If it is horizontal move.
        if start_pos[0] == end_pos[0]:
            if start_pos[1] < end_pos[1]:
                index = start_pos[1] + 1
                large_val = end_pos[1]
            else:
                index = end_pos[1] + 1
                large_val = start_pos[1]
            while index < large_val:
                if current_board.get_checker([start_pos[0], index]) != 'E':
                    return False
                index += 1

        # If it is vertical move.
        if start_pos[1] == end_pos[1]:
            if start_pos[0] < end_pos[0]:
                index = start_pos[0] + 1
                large_val = end_pos[0]
            else:
                index = end_pos[0] + 1
                large_val = start_pos[0]
            while index < large_val:
                if current_board.get_checker([index, start_pos[1]]) != 'E':
                    return False
                index += 1
        
        # If the start_pos and end_pos are at the same fortress and it is diagonal move.
        if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
            if abs(end_pos[0] - start_pos[0]) != abs(end_pos[1] - start_pos[1]):
                return False  
            if start_pos in current_board.get_blue_spec_pos() and end_pos in current_board.get_blue_spec_pos():
                return False
            if start_pos in current_board.get_red_spec_pos() and end_pos in current_board.get_red_spec_pos():
                return False
            if abs(end_pos[0] - start_pos[0]) == 2:
                index_1 = int((start_pos[0] + end_pos[0]) / 2)
                index_2 = int((start_pos[1] + end_pos[1]) / 2)
                if current_board.get_checker([index_1, index_2]) != 'E':
                    return False            
        return True
        
            
class Soldier(ChessPiece):
    """Represents a Soldier inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an Soldier object."""
        super().__init__(color)
        self._chess_piece_type = "Soldier"
    
    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists (contain start coord and end coord) and current board object. Checks if 
        the soldier can move from the start position to the end according to the movement rules of the soldier.
        """

        if start_pos == end_pos:    # Does not make move.
            return True

         # Blue player make move.   
        if self._color == "blue":
            if start_pos[0] - end_pos[0] not in [0, 1]: 
                    return False
            if abs(start_pos[1] - end_pos[1]) not in [0, 1]:
                return False
            if start_pos not in current_board.get_red_fortress() or end_pos not in current_board.get_red_fortress():
                if abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]):
                    return False
            else:
                if start_pos in current_board.get_red_spec_pos() and end_pos in current_board.get_red_spec_pos():
                    return False
        
        # Red player make move.
        if self._color == "red":
            if end_pos[0] - start_pos[0] not in [0, 1]: 
                return False
            if abs(start_pos[1] - end_pos[1]) not in [0, 1]:
                return False
            if start_pos not in current_board.get_blue_fortress() or end_pos not in current_board.get_blue_fortress():
                if abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]):
                    return False
            else:
                if start_pos in current_board.get_blue_spec_pos() and end_pos in current_board.get_blue_spec_pos():
                    return False
        return True


class Horse(ChessPiece):
    """Represents a Horse inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an Horse object."""
        super().__init__(color)
        self._chess_piece_type = "Horse"

    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists (contain start coord and end coord) and current board object. Checks if 
        the horse can move from the start position to the end according to the movement rules of the horse.
        """
        if start_pos == end_pos:    # Does not make move.
            return True
        
        if start_pos[0] - end_pos[0] == 2 and abs(start_pos[1] - end_pos[1]) == 1:
            if current_board.get_checker([start_pos[0] - 1, start_pos[1]]) == 'E':
                return True
        if start_pos[0] - end_pos[0] == -2 and abs(start_pos[1] - end_pos[1]) == 1:
            if current_board.get_checker([start_pos[0] + 1, start_pos[1]]) == 'E':
                return True
        if start_pos[1] - end_pos[1] == 2 and abs(start_pos[0] - end_pos[0]) == 1:
            if current_board.get_checker([start_pos[0], start_pos[1] - 1]) == 'E':
                return True
        if start_pos[1] - end_pos[1] == -2 and abs(start_pos[0] - end_pos[0]) == 1:
            if current_board.get_checker([start_pos[0], start_pos[1] + 1]) == 'E':
                return True   
        return False
    

class Elephant(ChessPiece):
    """Represents a Elephant inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an Elephant object."""
        super().__init__(color)
        self._chess_piece_type = "Elephant"
    
    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists (contain start coord and end coord) and current board object. Checks if 
        the elephant can move from the start position to the end according to the movement rules of the elephant.
        """
        if start_pos == end_pos:    # Does not make move.
            return True

        # if the end location is not correct.
        if abs(start_pos[0] - end_pos[0]) not in [2, 3] or abs(start_pos[1] - end_pos[1]) not in [2, 3]:
            return False
        if abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]):
            return False

        # if any obstacle betwween start and end position.
        if start_pos[0] - end_pos[0] == 3:
            if current_board.get_checker([start_pos[0] - 1, start_pos[1]]) != 'E':
                return False
            else:
                if start_pos[1] - end_pos[1] == 2:
                    if current_board.get_checker([start_pos[0] - 2, start_pos[1] - 1]) != 'E':
                        return False
                    else: 
                        return True
                if start_pos[1] - end_pos[1] == -2:
                    if current_board.get_checker([start_pos[0] - 2, start_pos[1] + 1]) != 'E':
                        return False
                    else: 
                        return True

        if start_pos[0] - end_pos[0] == -3:
            if current_board.get_checker([start_pos[0] + 1, start_pos[1]]) != 'E':
                return False
            else:
                if start_pos[1] - end_pos[1] == 2:
                    if current_board.get_checker([start_pos[0] + 2, start_pos[1] - 1]) != 'E':
                        return False
                    else: 
                        return True
                if start_pos[1] - end_pos[1] == -2:
                    if current_board.get_checker([start_pos[0] + 2, start_pos[1] + 1]) != 'E':
                        return False
                    else: 
                        return True
        
        if start_pos[1] - end_pos[1] == 3:
            if current_board.get_checker([start_pos[0], start_pos[1] - 1]) != 'E':
                return False
            else:
                if start_pos[0] - end_pos[0] == 2:
                    if current_board.get_checker([start_pos[0] - 1, start_pos[1] - 2]) != 'E':
                        return False
                    else:
                        return True
                if start_pos[0] - end_pos[0] == -2:
                    if current_board.get_checker([start_pos[0] + 1, start_pos[1] - 2]) != 'E':
                        return False
                    else:
                        return True
        
        if start_pos[1] - end_pos[1] == -3:
            if current_board.get_checker([start_pos[0], start_pos[1] + 1]) != 'E':
                return False
            else:
                if start_pos[0] - end_pos[0] == 2:
                    if current_board.get_checker([start_pos[0] - 1, start_pos[1] + 2]) != 'E':
                        return False
                    else:
                        return True
                if start_pos[0] - end_pos[0] == -2:
                    if current_board.get_checker([start_pos[0] + 1, start_pos[1] + 2]) != 'E':
                        return False
                    else:
                        return True


class Cannon(ChessPiece):
    """Represents a Cannon inherits from ChessPiece."""

    def __init__(self, color):
        """Creates an Cannon object."""
        super().__init__(color)
        self._chess_piece_type = "Cannon"
    
    def verify_move(self, start_pos, end_pos, current_board):
        """
        Takes as parameters two lists (contain start coord and end coord) and current board object. Checks if 
        the cannon can move from the start position to the end according to the movement rules of the cannon.
        """
        if start_pos == end_pos:    # Does not make move.
            return True

        # The piece at end_pos is cannon.
        if current_board.get_checker(end_pos) != 'E':
            if current_board.get_checker(end_pos).get_chess_piece_type() == "Cannon":
                return False 

        # If the start_pos and end_pos are not at the same fortress or both not at fortresses, and it is diagonal move return False.
        if start_pos not in current_board.get_blue_fortress() and start_pos not in current_board.get_red_fortress():
            if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                return False
        elif start_pos in current_board.get_blue_fortress(): 
            if end_pos not in current_board.get_blue_fortress():
                if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                    return False
        else:
            if end_pos not in current_board.get_red_fortress():
                if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
                    return False
        
        # The end location is next to start location.
        if abs(start_pos[0] - end_pos[0]) in [0, 1] and abs(start_pos[1] - end_pos[1]) in [0, 1]:
            return False 
        
        cannon_seat = 0
        # If it is horizontal move.
        if start_pos[0] == end_pos[0]:
            if start_pos[1] < end_pos[1]:
                index = start_pos[1] + 1
                large_val = end_pos[1]
            else:
                index = end_pos[1] + 1
                large_val = start_pos[1]
            while index < large_val:
                if current_board.get_checker([start_pos[0], index]) != 'E':
                    if current_board.get_checker([start_pos[0], index]).get_chess_piece_type() == "Cannon":
                        return False 
                    cannon_seat += 1
                index += 1
            if cannon_seat != 1:
                return False 
            return True

        # If it is vertical move.
        if start_pos[1] == end_pos[1]:
            if start_pos[0] < end_pos[0]:
                index = start_pos[0] + 1
                large_val = end_pos[0]
            else:
                index = end_pos[0] + 1
                large_val = start_pos[0]
            while index < large_val:
                if current_board.get_checker([index, start_pos[1]]) != 'E':
                    if current_board.get_checker([index, start_pos[1]]).get_chess_piece_type() == "Cannon":
                        return False
                    cannon_seat += 1
                index += 1
            if cannon_seat != 1:
                return False 
            return True
        
        # If the start_pos and end_pos are at the same fortress and it is diagonal move.
        if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
            if abs(end_pos[0] - start_pos[0]) != abs(end_pos[1] - start_pos[1]):
                return False  
            index_1 = int((start_pos[0] + end_pos[0]) / 2)
            index_2 = int((start_pos[1] + end_pos[1]) / 2)
            if current_board.get_checker([index_1, index_2]) != 'E':
                if current_board.get_checker([index_1, index_2]).get_chess_piece_type() != "Cannon":
                    return True
            return False


