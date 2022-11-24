from .ordering_heuristic import OrderingHeuristic
from ...search_tree.search_tree_node import SearchTreeNode


class ConstantHeuristic(OrderingHeuristic):
    def __init__(self, value: float = 0):
        self.value = value

    def potential(self, _: SearchTreeNode) -> float:
        return self.value
