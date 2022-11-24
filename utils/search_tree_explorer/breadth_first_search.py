import queue
import logging

from .search_tree_explorer import SearchTreeExplorer
from ..search_tree.search_tree_node import SearchTreeNode


class BreadthFirstSearch(SearchTreeExplorer):
    def __init__(self):
        logging.info("Using BreadthFirstSearch Search Tree Explorer")
        self.order: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
        self.best_solution_time: int = -1
        self.ITERATIONS_INCREMENT: int = 1

    def put(self, node: SearchTreeNode) -> None:
        # Avoid putting in nodes that would have been fathomed
        if self.best_solution_time == -1 or node.lower_bound < self.best_solution_time:
            self.order.put((node.level, node))

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        node: SearchTreeNode
        _, node = self.order.get()
        while (
            self.best_solution_time != -1
            and node.lower_bound >= self.best_solution_time
        ):
            _, node = self.order.get()
        return node, self.ITERATIONS_INCREMENT

    def finished(self) -> bool:
        if self.order.empty():
            logging.debug("Finishing as no more possible nodes")
            return True
        level_node_pair: tuple[int, SearchTreeNode]
        if all(
            map(
                lambda level_node_pair: level_node_pair[1].lower_bound
                >= self.best_solution_time,
                self.order.queue,
            )
        ):
            logging.debug("Finishing as there are no better solutions")
            return True
        return False

    def fathom(self, solution_time: int) -> None:
        if self.best_solution_time == -1 or solution_time < self.best_solution_time:
            self.best_solution_time = solution_time

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
