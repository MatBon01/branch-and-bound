import queue
import logging

from .search_tree_explorer import SearchTreeExplorer
from ..search_tree.search_tree_node import SearchTreeNode


class BreadthFirstSearch(SearchTreeExplorer):
    def __init__(self):
        logging.info("Using BreadthFirstSearch Search Tree Explorer")
        self.order: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
        self.ITERATIONS_INCREMENT: int = 1

    def put(self, node: SearchTreeNode) -> None:
        self.order.put((node.level, node))

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        node: SearchTreeNode
        _, node = self.order.get()
        return node, self.ITERATIONS_INCREMENT

    def finished(self) -> bool:
        return self.order.empty()

    def fathom(self, solution_time: int) -> None:
        pass

    def best(self) -> SearchTreeNode:
        # Return the node at the highest level with the lowest bound
        node: SearchTreeNode
        _, node = self.order.get()
        new_node: SearchTreeNode
        while not self.order.empty():
            _, new_node = self.order.get()
            # due to priority queue ordering this is the best node on the
            # deepest level
            if new_node.level > node.level:
                node = new_node
        return node
