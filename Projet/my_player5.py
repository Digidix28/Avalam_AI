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
import time
from avalam import *
import math

infinity = math.inf
class MyAgent(Agent):


    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in avalam.py.
        :param player: the player to control in this step (-1 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
            eg; (1, 4, 1 , 3) to move tower on cell (1,4) to cell (1,3)
        """

        print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        board = dict_to_board(percepts)
        
        start = time.time()
        v,move = h_alphabeta_search(player, board,step=step,treshhold=2)
        end = time.time()
        print('le move est : ', move,"\n")
        print('temps écoulé est : ', end - start)
        return move

    

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda state, depth: depth > d

def h_alphabeta_search(player, board, step,treshhold, h=lambda s , p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""
    

    def max_value(board, alpha, beta, depth):
        """board = board.clone()"""
        is_min = 1
        t = treshhold
        if(step >= 25):
            t = 5
        if board.is_finished():
            return player * board.get_score(), None
        if depth > t:
            return player * board.get_score(), None
        v, move = -infinity, None
        actions = list(board.get_actions_h2(player,is_min,step))
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
        is_min = -1
        t = treshhold
        if(step >= 25):
            t = 5
        if board.is_finished():
            return player * board.get_score(), None
        if depth > t:
            return player * board.get_score(), None

        v, move = +infinity, None
        actions = list(board.get_actions_h2(player,is_min,step))        
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

