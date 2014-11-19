"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def new_player(player):
    """
    helper function to swap player
    """
    if player == 3:
        return 2
    else:
        return 3

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    strategy = []
    if board.check_win() != None:
        return (SCORES[board.check_win()],(-1,-1))
    dummy_moves = board.get_empty_squares()
    for move in dummy_moves:
        temp_board = board.clone()
        temp_board.move(move[0], move[1], player)
        test = mm_move(temp_board.clone(),new_player(player))
        strategy.append((test[0],move))
   # print "my strategy", strategy, " on player: ", player      ##########
    cand = strategy[0]
    if player == provided.PLAYERX:
        for indx in range(len(strategy)):
            if strategy[indx][0] > cand[0]:
                cand = strategy[indx]
    else:
        for indx in range(len(strategy)):
            if strategy[indx][0] < cand[0]:
                cand = strategy[indx]
              
   # print "returning", cand, "\n\n"            ##########
    return cand

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERO)
