import math
from typing import Callable

from utils.search_tree.search_tree_node import SearchTreeNode

from .ordering_heuristic import OrderingHeuristic


class LevelHeuristic(OrderingHeuristic):
    def __init__(self, level_modifier: Callable[[int], float] = id):
        self.level_modifier = level_modifier

    def potential(self, node: SearchTreeNode) -> float:
        return self.level_modifier(node.level)


def reciprocal(num: int) -> float:
    if num == 0:
        return 0
    return 1.0 / float(num)


def id(num: int) -> float:
    return float(num)


def exponential_reciprocal(num: int) -> float:
    return 1.0 / (math.e ** float(num))
