# -*- coding: utf-8 -*-
"""
Common definitions for the Avalam players.
Copyright (C) 2010 - Vianney le Clément, UCLouvain
Modified by the teaching team of the course INF8215 - 2022, Polytechnique Montréal

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

PLAYER1 = 1
PLAYER2 = -1
import numpy as np
from avalam import InvalidAction

class MyBoard:

    """Representation of an Avalam Board.

    self.m is a self.rows by self.columns bi-dimensional array representing the
    board.  The absolute value of a cell is the height of the tower.  The sign
    is the color of the top-most counter (negative for red, positive for
    yellow).

    """

    # standard avalam
    max_height = 5
    initial_board = [ [ 0,  0,  1, -1,  0,  0,  0,  0,  0],
                      [ 0,  1, -1,  1, -1,  0,  0,  0,  0],
                      [ 0, -1,  1, -1,  1, -1,  1,  0,  0],
                      [ 0,  1, -1,  1, -1,  1, -1,  1, -1],
                      [ 1, -1,  1, -1,  0, -1,  1, -1,  1],
                      [-1,  1, -1,  1, -1,  1, -1,  1,  0],
                      [ 0,  0,  1, -1,  1, -1,  1, -1,  0],
                      [ 0,  0,  0,  0, -1,  1, -1,  1,  0],
                      [ 0,  0,  0,  0,  0, -1,  1,  0,  0] ]

    def __init__(self, percepts=initial_board, max_height=max_height,
                       invert=False):
        """Initialize the board.

        Arguments:
        percepts -- matrix representing the board
        invert -- whether to invert the sign of all values, inverting the
            players
        max_height -- maximum height of a tower

        """
        self.m = percepts
        self.rows = len(self.m)
        self.columns = len(self.m[0])
        self.max_height = max_height
        self.m = self.get_percepts(invert)  # make a copy of the percepts

    def __str__(self):
        def str_cell(i, j):
            x = self.m[i][j]
            if x:
                return "%+2d" % x
            else:
                return " ."
        return "\n".join(" ".join(str_cell(i, j) for j in range(self.columns))
                         for i in range(self.rows))

    def clone(self):
        """Return a clone of this object."""
        return MyBoard(self.m)

    def get_percepts(self, invert=False):
        """Return the percepts corresponding to the current state.

        If invert is True, the sign of all values is inverted to get the view
        of the other player.

        """
        mul = 1
        if invert:
            mul = -1
        return [[mul * self.m[i][j] for j in range(self.columns)]
                for i in range(self.rows)]

    def get_towers(self):
        """Yield all towers.

        Yield the towers as triplets (i, j, h):
        i -- row number of the tower
        j -- column number of the tower
        h -- height of the tower (absolute value) and owner (sign)

        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j]:
                    yield (i, j, self.m[i][j])

    def is_action_valid(self, action):
        """Return whether action is a valid action."""
        try:
            i1, j1, i2, j2 = action
            if i1 < 0 or j1 < 0 or i2 < 0 or j2 < 0 or \
               i1 >= self.rows or j1 >= self.columns or \
               i2 >= self.rows or j2 >= self.columns or \
               (i1 == i2 and j1 == j2) or (abs(i1-i2) > 1) or (abs(j1-j2) > 1):
                return False
            h1 = abs(self.m[i1][j1])
            h2 = abs(self.m[i2][j2])
            if h1 <= 0 or h1 >= self.max_height or h2 <= 0 or \
                    h2 >= self.max_height or h1+h2 > self.max_height:
                return False
            return True
        except (TypeError, ValueError):
            return False

    def get_tower_actions(self, i, j):
        """Yield all actions with moving tower (i,j)"""
        h = abs(self.m[i][j])
        if h > 0 and h < self.max_height:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    action = (i, j, i+di, j+dj)
                    if self.is_action_valid(action):
                        yield action

    def is_tower_movable(self, i, j):
        """Return wether tower (i,j) is movable"""
        for action in self.get_tower_actions(i, j):
            return True
        return False

    def actions_heuristic1(self,action,player):
        """Notre heuristique qui empêche de jouer des moves qui posent une tour adverse sur la notre"""
        i,j,k,l = action 
        is_good_action = True
        if (player * self.m[i][j]) < 0:
            if (player * self.m[k][l]) > 0:
                is_good_action = False
        return is_good_action

    def actions_heuristic2(self,action,player):
        """Notre heuristique qui empêche de jouer des moves qui créent des tours de taille 4."""
        i,j,k,l = action      
        return (abs(self.m[i][j]) +abs(self.m[k][l])) != 4

    def actions_heuristic3(self,action):
        """Notre heuristique qui empêche de jouer des moves qui créent des complémentaires avec les tours adverses."""
        clone = self.clone().play_action(action)
        i,j,k,l = action  #[k,l] correspond à la position de la nouvelle tour formée
        is_comlementary = False
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if clone.is_action_valid((k,l,k+di,l+dj)):
                    if abs(clone.m[k+di][l+dj]) + abs(clone.m[k][l]) == 5 :
                        is_comlementary = True
        return not(is_comlementary)

    def get_actions_h(self,player,step,is_min):
        """Yield all valid actions on this board."""

        if(step > 10 and step <= 19):
            for i, j, h in self.get_towers():
                for action in self.get_tower_actions(i, j):
                    if self.actions_heuristic1(action=action,player=player):
                        if self.actions_heuristic3(action):
                            yield action
        elif(step<24):
            for i, j, h in self.get_towers():
                for action in self.get_tower_actions(i, j):
                    if self.actions_heuristic1(action=action,player=player):
                        if self.actions_heuristic2(action,player):
                            yield action
        else:
            for i, j, h in self.get_towers():
                    for action in self.get_tower_actions(i, j):
                        if self.actions_heuristic1(action,player):
                                    yield action


    def get_actions_h2(self,player,is_min,step):
        """Yield all valid actions on this board."""
        for i, j, h in self.get_towers():
                for action in self.get_tower_actions(i, j):
                    if self.actions_heuristic(action,player,is_min):
                            if self.actions_heuristic2(action,player,is_min):
                                yield action
    

    def get_actions(self):
        """Yield all valid actions on this board."""
        for i, j, h in self.get_towers():
            for action in self.get_tower_actions(i, j):
                yield action
    
    # def actions_heuristic(self,action,player,is_min):
    #     """Yield all valid actions on this board."""
    #     i,j,k,l = action      
    #     return not(is_min * player * self.m[i][j] < 0 and is_min * player * self.m[k][l] > 0)

    def get_tower_5(self,action,player,is_min):
        """Yield all valid actions on this board."""
        i,j,k,l = action      
        return not(is_min * player * self.m[i][j] < 0 and is_min * player * self.m[k][l] > 0)

    

    def get_opponent_move(self,board):
        if board == None:
            return None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j] - board.m[i][j] !=0 :
                    return (i,j)

    def get_close_actions(self,opp_move : tuple):
        """Yield all valid actions on this board."""
        if opp_move == None : 
            return self.get_actions
        a,b = opp_move
        for i, j, h in self.get_towers() :
            if(np.linalg.norm(np.array([i,j]) - np.array([a,b])) <= 2.9):
                for action in self.get_tower_actions(i, j):
                    yield action


    def play_action(self, action):
        """Play an action if it is valid.

        An action is a 4-uple containing the row and column of the tower to
        move and the row and column of the tower to gobble. If the action is
        invalid, raise an InvalidAction exception. Return self.

        """
        if not self.is_action_valid(action):

            print("ca vient de l'intérieur : ",action,"\n")
            print("board : \n", self)
            raise InvalidAction(action)
        i1, j1, i2, j2 = action
        h1 = abs(self.m[i1][j1])
        h2 = abs(self.m[i2][j2])
        if self.m[i1][j1] < 0:
            self.m[i2][j2] = -(h1 + h2)
        else:
            self.m[i2][j2] = h1 + h2
        self.m[i1][j1] = 0
        return self

    def is_finished(self):
        """Return whether no more moves can be made (i.e., game finished)."""
        for action in self.get_actions():
            return False
        return True

    def get_score(self):
        """Return a score for this board.

        The score is the difference between the number of towers of each
        player. In case of ties, it is the difference between the maximal
        height towers of each player. If self.is_finished() returns True,
        this score represents the winner (<0: red, >0: yellow, 0: draw).

        """
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j] < 0:
                    score -= 1
                elif self.m[i][j] > 0:
                    score += 1
        if score == 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.m[i][j] == -self.max_height:
                        score -= 1
                    elif self.m[i][j] == self.max_height:
                        score += 1
        return score

    def get_score2(self):
        """Return a score for this board.

        The score is the difference between the number of towers of each
        player. In case of ties, it is the difference between the maximal
        height towers of each player. If self.is_finished() returns True,
        this score represents the winner (<0: red, >0: yellow, 0: draw).

        """
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j] < 0:
                    score -= 1
                elif self.m[i][j] > 0:
                    score += 1
        if score == 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.m[i][j] == -self.max_height:
                        score -= 1
                    elif self.m[i][j] == self.max_height:
                        score += 1
            score = score / 50
        return score

    def get_score3(self):
        """Return a score for this board.

        The score is the difference between the number of towers of each
        player. In case of ties, it is the difference between the maximal
        height towers of each player. If self.is_finished() returns True,
        this score represents the winner (<0: red, >0: yellow, 0: draw).

        """
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                score += self.m[i][j]
        if score == 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.m[i][j] == -self.max_height:
                        score -= 1
                    elif self.m[i][j] == self.max_height:
                        score += 1
            score = score / 50
        return score

    def baseline_h(self):
        
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if (self.m[i][j] == 5) :
                    score += 1
                if (not self.is_tower_movable(i,j)):
                    score +=1
            
        
        return score/50


def my_dict_to_board(dictio):
    """Return a clone of the board object encoded as a dictionary."""
    clone_board = MyBoard()
    clone_board.m = dictio['m']
    clone_board.rows = dictio['rows']
    clone_board.max_height = dictio['max_height']

    return clone_board

