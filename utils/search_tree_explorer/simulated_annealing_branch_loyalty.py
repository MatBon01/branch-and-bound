import queue
import random

from .search_tree_explorer import SearchTreeExplorer
from .ordering_heuristic.ordering_heuristic import OrderingHeuristic
from .ordering_heuristic.constant_heuristic import ConstantHeuristic
from ..search_tree.search_tree_node import SearchTreeNode


class SimulatedAnnealingBranchLoyalty(SearchTreeExplorer):
    def __init__(
        self,
        heuristic: OrderingHeuristic = ConstantHeuristic(),
        seed: int = 1234567890,
        initial_temperature: float = 1,
    ):
        random.seed(seed)
        self.heuristic: OrderingHeuristic = heuristic
        self.nodes: queue.PriorityQueue[
            tuple[float, SearchTreeNode]
        ] = queue.PriorityQueue()
        self.last_children: queue.PriorityQueue[tuple[float, SearchTreeNode]] = []
        self.ITERATIONS_INCREMENT: int = 1
        self.loyalty_rate: float = -1
        self.INITIAL_TEMPERATURE: float = initial_temperature
        self.temperature: float = initial_temperature

    def put(self, node: SearchTreeNode) -> None:
        self.last_children.put((self.heuristic(node), node))

    def _continue_on_branch(self) -> bool:
        # TODO:: finish
        return not self.last_children.empty()

    def _empty_children_list(self) -> None:
        # empty the children list
        old_child_pair: tuple[float, SearchTreeNode]
        while not self.last_children.empty():
            old_child_pair = self.last_children.get()
            self.nodes.put(old_child_pair)

    def _initialise_temperature(self) -> None:
        # Prevents division by 0 errors
        if self.nodes.empty() and self.last_children.empty():
            self.temperature = self.INITIAL_TEMPERATURE
            return

        # Calculate the averages of the heuristics
        count: int = 0
        heuristic_sum: float = 0
        heuristic: float
        for heuristic, _ in self.nodes.queue:
            heuristic_sum += heuristic
            count += 1

        for heuristic, _ in self.last_children.queue:
            heuristic_sum += heuristic
            count += 1

        self.temperature = heuristic_sum / count

    def _initialise_new_search(self) -> None:
        self._empty_children_list()
        self._initialise_temperature()

    def _calculate_and_set_loyalty_rate(self, current_heuristic: float) -> None:
        if self.nodes.empty():
            return 0  # forces us to start again with this node as the new root

        # Get next best node from the list of nodes
        next_best_heuristic: float  # we know this number is >= to current_heuristic
        next_best_node: SearchTreeNode
        next_best_heuristic, next_best_node = self.nodes.get()
        self.nodes.put((next_best_heuristic, next_best_node))

        # sets the loyalty rate depending on how much more promising this
        # node is
        self.loyalty_rate = 1 - (next_best_heuristic / current_heuristic)

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        # calculate the probability of continuing on this node
        if self._continue_on_branch():  # also includes not having more branches
            next_child: SearchTreeNode
            _, next_child = self.last_children.get()
            self.temperature = self.loyalty_rate * self.temperature
            return next_child, self.ITERATIONS_INCREMENT
        else:
            self._initialise_new_search()

            best_node: SearchTreeNode
            best_heuristic, best_node = self.nodes.get()
            self._calculate_and_set_loyalty_rate(best_heuristic)

            return best_node

    def finished(self) -> bool:
        return self.last_children.empty() and self.nodes.empty()

    def fathom(self, solution_time: int) -> None:
        current_heuristic: float
        current_node: SearchTreeNode

        last_children_replacement: queue.PriorityQueue[
            tuple[float, SearchTreeNode]
        ] = queue.PriorityQueue()
        while not self.last_children.empty():
            current_heuristic, current_node = self.last_children.get()
            if current_node.lower_bound < solution_time:
                last_children_replacement.put((current_heuristic, current_node))
        self.last_children = last_children_replacement

        nodes_replacement: queue.PriorityQueue[
            tuple[float, SearchTreeNode]
        ] = queue.PriorityQueue()
        while not self.nodes.empty:
            current_heuristic, current_node = self.nodes.get()
            if current_node.lower_bound < solution_time:
                nodes_replacement.put((current_heuristic, current_node))
        self.nodes = nodes_replacement

    def best(self) -> SearchTreeNode:
        if self.last_children.empty():
            best_node: SearchTreeNode
            _, best_node = self.nodes.get()
            return best_node

        if self.nodes.empty():
            best_node: SearchTreeNode
            _, best_node = self.last_children.get()
            return best_node

        last_child_pair: SearchTreeNode = self.last_children.get()
        nodes_pair: SearchTreeNode = self.nodes.get()

        best_node: SearchTreeNode
        if nodes_pair > last_child_pair:
            self.last_children.put(last_child_pair)
            _, best_node = nodes_pair
        else:
            self.nodes.put(nodes_pair)
            _, best_node = last_child_pair
        return best_node

    def __len__(self) -> int:
        return len(self.nodes) + len(self.last_children)
