#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
from avalam import *
import math

infinity = math.inf
class MyAgent(Agent):


    """This agent is the basic one, it just uses a custom heuristic instead of the baseline
    board.get_score
    """

    def play(self, percepts, player, step, time_left):
     

        print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        board = dict_to_board(percepts)
        
        "start = time.time()"
        v,move = h_alphabeta_search(player, board)
        "end = time.time()"
        "print('temps écoulé est : ', end - start)"
        return move

    

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda state, depth: depth > d

def h_alphabeta_search(player, board, h=lambda s , p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""
    

    def max_value(board, alpha, beta, depth):
        """board = board.clone()"""
        if board.is_finished():
            return player * board.get_score(), None
        if depth > 2:
            return player * board.get_score2(), None
        v, move = -infinity, None
        actions = list(board.get_actions())
        for a in actions:
            next_board = board.clone().play_action(a)
            v2, _ = min_value(next_board, alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                   
                return v, move     
        
        return v, move

    def min_value(board, alpha, beta, depth):
        """ board = board.clone()"""
        if board.is_finished():
            return player * board.get_score(), None
        if depth > 2:
            return player * board.get_score2(), None

        v, move = +infinity, None
        actions = list(board.get_actions())        
        for a in actions:
            next_board = board.clone().play_action(a)
            v2, _ = max_value(next_board, alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(board, -infinity, +infinity, 0)

if __name__ == "__main__":
    agent_main(MyAgent())

