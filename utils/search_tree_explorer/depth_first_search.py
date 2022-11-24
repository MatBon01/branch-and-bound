import logging
import queue
from typing import Optional

from ..search_tree.search_tree_node import SearchTreeNode
from .search_tree_explorer import SearchTreeExplorer


class DepthFirstSearch(SearchTreeExplorer):
    def __init__(self, one_depth: bool = False):
        logging.info("Using DepthFirstSearch Search Tree Explorer")
        self.order: queue.PriorityQueue[
            tuple[int, SearchTreeNode]
        ] = queue.PriorityQueue()
        self.one_depth: bool = one_depth
        self.last_node: Optional[SearchTreeNode] = None
        self.ITERATIONS_INCREMENT: int = 1
        self.min_solution_time: int = -1

    def put(self, node: SearchTreeNode) -> None:
        # queue ordered by smallest element but want largest level first so
        # we negate and have node compared by tardiness minimised
        self.order.put((-node.level, node))

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        _, node = self.order.get()

        # Skip over nodes that have been "removed" via fathoming
        while (
            self.min_solution_time != -1 and node.lower_bound >= self.min_solution_time
        ):
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
        if self.min_solution_time != -1:
            if all(
                node.lower_bound >= self.min_solution_time
                for _, node in self.order.queue
            ):
                logging.debug("Finishing as there are no better solutions")
                return True
        return False

    def fathom(self, solution_time: int) -> None:
        if self.min_solution_time == -1 or solution_time < self.min_solution_time:
            self.min_solution_time = solution_time

    def best(self) -> SearchTreeNode:
        node, _ = self.next()
        return node
    
    def deepest(self) -> SearchTreeNode:
        node, _ = self.next()
        return node

    def __len__(self) -> int:
        return len(self.order.queue)
