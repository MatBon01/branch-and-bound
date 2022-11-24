from typing import Callable

from utils.search_tree.search_tree_node import SearchTreeNode

from .ordering_heuristic import OrderingHeuristic


class LevelHeuristic(OrderingHeuristic):
    def __init__(self, level_modifier: Callable[[int], float]):
        super().__init__()
        self.level_modifier = level_modifier

    def potential(self, node: SearchTreeNode) -> float:
        return self.level_modifier(node.level)
