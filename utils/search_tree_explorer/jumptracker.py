import logging
import queue

from ..search_tree.search_tree_node import SearchTreeNode
from .search_tree_explorer import SearchTreeExplorer


class JumpTracker(SearchTreeExplorer):
    def __init__(self):
        logging.info("Using JumpTracker Search Tree Explorer")
        self.nodes: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
        self.ITERATIONS_INCREMENT: int = 1

    def put(self, node: SearchTreeNode) -> None:
        self.nodes.put(node)

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        return self.nodes.get(), self.ITERATIONS_INCREMENT

    def finished(self) -> bool:
        if self.nodes.empty():
            logging.debug("Finishing as no more possible nodes")
            return True
        if self.nodes.queue[0].terminated:
            logging.debug("Finishing as there are no better solutions")
            return True
        return False

    def fathom(self, solution_time: int) -> bool:
        # Add a node that indicates stopping by making it terminal
        self.nodes.put(SearchTreeNode([], [], None, solution_time))

    def best(self) -> SearchTreeNode:
        node, _ = self.next()
        return node

    def __len__(self) -> int:
        return len(self.nodes.queue)