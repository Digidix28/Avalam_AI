
import random
from typing import List, Set, Tuple
from avalam import *
from Node import Node


class Tree:
    """Tree representing a MCTS tree"""
    def __init__(self, player: int = 0, initial_board: Board = None):
        """
        Tree constructor
        Args:
            player (int): The player
            initial_board (CustomBoard): The initial board
        """
        opponent = - player
        self.root = Node(player=opponent, board=initial_board, action=None,
                             U=0, N=0)


    def getInterestingNode(self) -> Node:

        node = self.root
        while len(node.children) != 0 and node.N > 0:
            all_ucts = list(map(lambda child: child.get_uct_value(), node.children))
            max_uct = max(all_ucts)
            nodes_max_uct = [node.children[i] for i in range(len(node.children)) if all_ucts[i] == max_uct]
            node = random.choice(nodes_max_uct)

        return node

    @staticmethod
    def getPlayersFromNode(nodePlayer):
        return - nodePlayer, nodePlayer

    def expand(self, node: Node):

        current_board = node.board
        if current_board.is_finished():
            return node

        player, opponent = self.getPlayersFromNode(node.player)

        for action in current_board.get_actions():
            new_board = current_board.clone()
            new_board.play_action(action)
            node.addChild(Node(player=player, action=action, board=new_board))

        return random.choice(node.children)

    def simulate(self, node: Node):

        board = node.board
        player, opponent = self.getPlayersFromNode(node.player)

        return player * board.get_score()

    def backPropagate(self, node: Node, simulation_result: int):


        while node:
            node.U += simulation_result
            node.N += 1
            node = node.parent


    def get_best_child_action(self) -> Tuple[str, int, int]:

        player, opponent = self.getPlayersFromNode(self.root.player)
        nodes_max_N = [node for node in self.root.children if node.N == max(list(map(lambda child: child.N, self.root.children)))]

        return self.get_random_node(nodes_max_N).action

    @staticmethod
    def get_random_node(nodes) -> Node:

        return random.choice(nodes)

    def separate_pawns_walls_nodes(self, nodes: List[Node]) -> Tuple[List[Node], List[Node]]:

        pawns_nodes = []
        walls_nodes = []
        for node in nodes:
            if node.action[0] == 'P':
                pawns_nodes.append(node)
            else:
                walls_nodes.append(node)
        return pawns_nodes, walls_nodes

    def get_node_gain(self, node: Node) -> int:
        
        player, opponent = self.getPlayersFromNode(self.root.player)
        if node.action[0] == "P":
            return self.root.board.min_steps_before_victory_safe(player) - node.board.min_steps_before_victory_safe(player)
        else:
            opponentGain = node.board.min_steps_before_victory_safe(opponent) - self.root.board.min_steps_before_victory_safe(opponent)
            playerGain = node.board.min_steps_before_victory_safe(player) - self.root.board.min_steps_before_victory_safe(player)
            return opponentGain - playerGain
