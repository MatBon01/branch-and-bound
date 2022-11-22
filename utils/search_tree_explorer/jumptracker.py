import queue

from ..search_tree.search_tree_node import SearchTreeNode
from .search_tree_explorer import SearchTreeExplorer


class JumpTracker(SearchTreeExplorer):
    def __init__(self):
        self.nodes: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
        self.ITERATIONS_INCREMENT: int = 1

    def put(self, node: SearchTreeNode) -> None:
        self.nodes.put(node)

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        return self.nodes.get(), self.ITERATIONS_INCREMENT

    def finished(self) -> bool:
        return self.nodes.empty()
