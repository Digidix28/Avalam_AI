# ####################################################################
# # 		* Simon, Sanmar (1938126)
# # 		* Harti, Ghali (1953494)
# ####################################################################

from __future__ import annotations

from math import log, sqrt
from typing import List, Tuple
from avalam import *



class Node:

    def __init__(self, player: int = 1, action: Tuple[str, int, int] = None,
                 following_shortest_path: bool = False,
                 board: Board = None, U: int = 0, N: int = 0):
 

        self.player = player
        self.action = action
        self.board = board
        self.U = U
        self.N = N
        self.children: List[Node]
        self.children = []
        self.parent = None

    def addChild(self, child: Node):

        child.parent = self
        self.children.append(child)

    def get_uct_value(self) -> float:

        N = self.N
        if N == 0:
            return float('inf')
        else:
            N_parent = self.parent.N
            U = self.U
            return (U / N) + sqrt(2) * sqrt(log(N_parent) / N)