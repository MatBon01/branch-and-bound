import logging
import queue
from typing import Optional

from ..search_tree.search_tree_node import SearchTreeNode
from .search_tree_explorer import SearchTreeExplorer
from .ordering_heuristic.ordering_heuristic import OrderingHeuristic
from .ordering_heuristic.constant_heuristic import ConstantHeuristic


class JumpTracker(SearchTreeExplorer):
    def __init__(self, heuristic: OrderingHeuristic = ConstantHeuristic()):
        logging.info("Using JumpTracker Search Tree Explorer")
        self.nodes: queue.PriorityQueue[
            tuple[float, SearchTreeNode]
        ] = queue.PriorityQueue()
        self.ITERATIONS_INCREMENT: int = 1
        self.heuristic: OrderingHeuristic = heuristic

    def put(self, node: SearchTreeNode) -> None:
        self.nodes.put((self.heuristic.potential(node), node))

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        node: SearchTreeNode
        _, node = self.nodes.get()
        return node, self.ITERATIONS_INCREMENT

    def finished(self) -> bool:
        return self.nodes.empty()

    def fathom(self, solution_time: int) -> None:
        # Add a node that indicates stopping by making it terminal
        count: int = 0
        new_queue: queue.PriorityQueue[
            tuple[float, SearchTreeNode]
        ] = queue.PriorityQueue()
        heuristic: float
        node: SearchTreeNode
        for heuristic, node in self.nodes.queue:
            if node.lower_bound < solution_time:
                new_queue.put((heuristic, node))
            else:
                count += 1
        logging.debug("%d nodes removed by fathoming", count)
        self.nodes = new_queue

    def best(self) -> SearchTreeNode:
        # returns the most promising node (by heuristic)
        node, _ = self.next()
        return node

    def deepest(self) -> SearchTreeNode:
        q = queue.PriorityQueue()

        for _, node in self.nodes.queue:
            q.put((-node.level, node))

        _, node = q.get()
        return node

    def __len__(self) -> int:
        return len(self.nodes.queue)
