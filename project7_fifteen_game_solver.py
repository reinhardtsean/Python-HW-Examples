"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
http://www.codeskulptor.org/#user37_1ca8cMCkdd_27.py
"""

import poc_fifteen_gui
import codeskulptor
codeskulptor.set_timeout(5)

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":                
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
    
    
    def zone1(self, zero_pos, c_pos):
        """
        Zone 1 Helper Function
        """
        moves = ''
        over = zero_pos[1] - c_pos[1]
        #move the zero tile over the target tile
        for dummy_o in range(over):
            moves += 'l'
        over -= 1
        while over > 0:
            moves += 'urrdl'
            over -= 1
        return moves
    
    def zone1b(self, zero_pos, c_pos):
        """
        Zone 1b Helper Function
        """
        moves = ''
        over = zero_pos[1] - c_pos[1]
        #move the zero tile over the target tile
        for dummy_o in range(over):
            moves += 'l'
        over -= 1
        moves += 'urdl'
        while over > 0:
            moves += 'urrdl'
            over -= 1
        return moves
    
    def zone2(self, zero_pos, c_pos):
        """
        Zone 2 Helper Function
        """
        moves = ''
        over = zero_pos[0] - c_pos[0]
        #move the zero tile over the target tile
        for dummy_o in range(over):
            moves += 'u'
        over -= 1
        while over > 0:
            moves += 'lddru'
            over -= 1
        
        return moves
    
    def zone3(self, zero_pos, c_pos):
        """
        Zone 3 Helper Function
        """
        moves = ''
        # move zero tile up to same row
        over1 = zero_pos[0] - c_pos[0]
        for dummy_o in range(over1):
            moves += 'u'
        over2 = c_pos[1] - zero_pos[1]
        for dummy_o in range(over2):
            moves += 'r'
        over2 -= 1
        # Pull the target tile into the same column as the zero
        #C1 target tile was not in 0'th row
        if c_pos[0] != 0:
            while over2 > 0:
                moves += 'ulldr'
                over2 -= 1
        else:
            while over2 > 0:
                moves += 'dllur'
                over2 -= 1
        # locate zero tile under target tile and prep for next iteration
        #C1 target tile was not in 0'th row
        if c_pos[0] != 0:
            moves += 'ullddr'
        else:   
            moves += 'dl'
        over1 -= 1
        while over1 > 0:
            moves += 'd'
            over1 -=1
        return moves
        
    def zone4(self, zero_pos, c_pos):
        """
        Zone 4 Helper Function
        """
        moves = ''
        # move zero tile up to same row
        over1 = zero_pos[0] - c_pos[0]
        for dummy_o in range(over1):
            moves += 'u'
        over2 = zero_pos[1] - c_pos[1]
        for dummy_o in range(over2):
            moves += 'l'
        over2 -= 1
        # Pull the target tile into the same column as the zero
        while over2 > 0:
            if c_pos[0] == 0:
                moves += 'drrul'
            else:
                moves += 'urrdl'
            over2 -= 1
        
        return moves
        
        
    
    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        num_start = target_row*self._width + target_col+1
        if self.get_number(target_row, target_col) != 0:
            return False
        tcol = (target_col+1) % self._width
        trow = target_row + (target_col+1)/self._width
        for inx in range(num_start,self._height*self._width):
            targ = self.get_number(trow, tcol)
            if targ != inx:
                return False
            trow = trow + (tcol+1)/self._width
            tcol = (tcol+1)% self._width
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        c_pos = self.current_position(target_row, target_col)
        zero_pos = [target_row, target_col]
        moves = ""
        in_pos = False
        
        while in_pos == False:
            # zone 1 - Target on same row:
            if c_pos[0] == zero_pos[0]:
                moves += self.zone1(zero_pos, c_pos)
                in_pos = True
            
            # zone 2 - Target on same column
            elif c_pos[1] == zero_pos[1]:
                moves += self.zone2(zero_pos, c_pos)
                moves += 'ld'
                in_pos = True
                
            # zone 3 - Target above and to the right of zero
            elif c_pos[1] > zero_pos[1]:      
                moves += self.zone3(zero_pos, c_pos)
                curr1 = c_pos[0]
                curr2 = zero_pos[1]
                c_pos = (curr1, curr2)
            
            # zone 4
            else:
                moves += self.zone4(zero_pos, c_pos)
                # locate zero tile under target tile and prep for next iteration
                #C1 target tile was not in 0'th row
                moves += 'dr'
                over1 = zero_pos[0] - c_pos[0] - 1
                while over1 > 0:
                    moves += 'd'
                    over1 -=1
                curr1 = c_pos[0]
                curr2 = zero_pos[1]
                c_pos = (curr1, curr2)
    
        
        self.update_puzzle(moves)
        assert self.lower_row_invariant(target_row, target_col-1)
        return moves

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        c_pos = self.current_position(target_row, 0)
        zero_pos = [target_row, 0]
        moves = 'ur'
        moves_2 = ""
        self.update_puzzle(moves)
        c2_pos = self.current_position(target_row, 0)
        zero_pos = [target_row-1, 1]
        if c2_pos[0] == target_row and c2_pos[1] == 0:
            ### Move the zero tile
            mov = self._width - 2
            for dummy_i in range(mov):
                moves_2 += 'r'
            self.update_puzzle(moves_2)
            return moves +moves_2
        else:
            # zone 2 - Target on same column
            if c2_pos[1] == zero_pos[1]:
                moves_2 += self.zone2(zero_pos, c2_pos)
                moves_2 += 'ld'          
            # zone 3 - Target above and to the right of zero
            elif c_pos[1] > zero_pos[1]:      
                moves_2 += self.zone3(zero_pos, c2_pos)

                curr1 = c2_pos[0]
                curr2 = zero_pos[1]
                c2_pos = (curr1, curr2)    
                moves_2 += self.zone2(zero_pos, c2_pos)
                moves_2 += 'ld'
            else:
                moves_2 += self.zone4(zero_pos, c2_pos)
                curr1 = c2_pos[0]
                curr2 = zero_pos[1]
                c2_pos = (curr1, curr2)    
                moves_2 += self.zone2(zero_pos, c2_pos)
            
            # Perform 3x2 swap
            moves_2 += 'ruldrdlurdluurddlur'
            
            ### Move the zero tile
            mov = self._width - 2
            for dummy_i in range(mov):
                moves_2 += 'r'
            self.update_puzzle(moves_2)
            assert self.lower_row_invariant(target_row-1, self._width-1)
            return moves + moves_2
    
    
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        num_start = target_col+1

        if self.get_number(0, target_col) != 0:
            return False
        tcol = (target_col+1) % self._width
        trow = 0 + (target_col+1)/self._width
        for inx in range(num_start,self._height*self._width):
            targ = self.get_number(trow, tcol)
            if not(trow == 1 and tcol < target_col) and targ != inx:
                return False
            trow = trow + (tcol+1)/self._width
            tcol = (tcol+1)% self._width
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.lower_row_invariant(1, target_col) == False:
            return False
        num_start = target_col +1
        tcol = num_start
        for inx in range(num_start,self._width):
            targ = self.get_number(0, tcol)
            if targ != inx:
                return False
            tcol = (tcol+1)% self._width
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        c_pos = self.current_position(0, target_col)
        zero_pos = [0, target_col]
        moves = 'ld'
        moves2 = ""
        self.update_puzzle(moves)
        c2_pos = self.current_position(0,target_col)
        zero_pos = [1, target_col-1]
        if c2_pos[0] == 0 and c2_pos[1] == target_col:
            return moves
        else:
            # zone 1 - Target on same row
            if c2_pos[0] == zero_pos[0]:
                moves2 = ''
                over = zero_pos[1] - c_pos[1]
                #move the zero tile over the target tile
                for dummy_o in range(over):
                    moves2 += 'l'
                over -= 1
                while over > 0:
                    moves2 += 'urrdl'
                    over -= 1          
            
            # zone 4 - Target above and to the left of zero
            else:
                moves2 = ''
                over = zero_pos[1] - c_pos[1]
                #move the zero tile over the target tile
                for dummy_o in range(over):
                    moves2 += 'l'
                over -= 1
                moves2 += 'urdl'
                while over > 0:
                    moves2 += 'urrdl'
                    over -= 1

            moves2 += 'urdlurrdluldrruld'
            
            self.update_puzzle(moves2)
            assert self.row1_invariant(target_col-1)
            return moves + moves2
            
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        c_pos = self.current_position(1, target_col)
        zero_pos = [1, target_col]
        moves = ""

        # zone 1 - Target on same row:
        if c_pos[0] == zero_pos[0]:
            
            moves += self.zone1(zero_pos, c_pos)
        else:
            moves += self.zone1b(zero_pos, c_pos)

         
        moves += 'ur'
        self.update_puzzle(moves)
        assert self.row0_invariant(target_col)
        return moves

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        abc = self._width
        moves = 'lu'
        self.update_puzzle('lu')
        p_state = {(0,0):0,(0,1):1,(1,0):abc,(1,1):abc+1}
        index = 0
        while index < 4:
            if self.get_number(0,0) == p_state[(0,0)] and self.get_number(0,1) == p_state[(0,1)] and self.get_number(1,0) == p_state[(1,0)] and self.get_number(1,1) == p_state[(1,1)]:
                return moves
            else:
                moves += 'rdlu'
                self.update_puzzle('rdlu')
                index +=1
        return None
        
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        
        full_moves = ''
        zeromove = ''
        #move zero to bottom corner
        zero_pos = self.current_position(0,0)
        for dummy_over in range(self._height-1-zero_pos[0]):
            zeromove += 'd'
        for dummy_down in range(self._width-1-zero_pos[1]):
            zeromove += 'r'
        full_moves += zeromove
        self.update_puzzle(zeromove)
        

        #perform solve on rows until last two
        for rows in range(self._height - 2):
            target_row = self._height-1-rows
            for cols in range(self._width-1):
                target_cols = self._height-1-cols
                self.lower_row_invariant(target_row, target_cols )
                full_moves += self.solve_interior_tile(target_row, target_cols)
            self.lower_row_invariant(target_row,0)   
            full_moves += self.solve_col0_tile(target_row)    
         
        # Perform 2x2 RH Iteration
        for col in range(self._width-2):
            target_col = self._width-1-col
            self.row1_invariant(target_col)
            full_moves += self.solve_row1_tile(target_col)
            self.row0_invariant(target_col)
            full_moves += self.solve_row0_tile(target_col)

        # Perform final 2x2 sort
        full_moves += self.solve_2x2()
        
        return full_moves
    
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

