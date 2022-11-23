import logging
import queue

from ..search_tree.search_tree_node import SearchTreeNode
from .search_tree_explorer import SearchTreeExplorer


class DepthFirstSearch(SearchTreeExplorer):
    def __init__(self, one_depth=False):
        logging.info("Using depth first search search tree explorer")
        self.order: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
        self.one_depth: bool = one_depth
        self.last_node: SearchTreeNode = None
        self.ITERATIONS_INCREMENT: int = 1

    def put(self, node: SearchTreeNode) -> None:
        # queue ordered by smallest element but want largest level first so
        # we negate and have node compared by tardiness minimised
        self.order.put((-node.level, node))

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        _, node = self.order.get()
        self.last_node = node
        return node, self.ITERATIONS_INCREMENT

    def finished(self) -> bool:
        if self.order.empty():
            logging.debug("Finishing as no more possible nodes")
            return True
        if self.one_depth and self.last_node is not None and self.last_node.terminated:
            logging.debug("Finishing as one depth search and last node is terminal")
            return True
        return False
