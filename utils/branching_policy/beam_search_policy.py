import logging
import queue
from typing import Callable
from utils.bounding_policy.bounding_policy import BoundingPolicy
from utils.branching_policy.branching_policy import BranchingPolicy
from utils.job_dependencies.graph import Job
from utils.job_dependencies.job_dependency_graph import JobDependencyGraph
from ..search_tree.search_tree_node import SearchTreeNode


class BeamSearchPolicy(BranchingPolicy):
    def __init__(
        self,
        jobs: JobDependencyGraph,
        bounding_policy: BoundingPolicy,
        w: Callable[[int], int],
    ):
        logging.info("Using Beam Search Branching Policy")
        self.jobs: JobDependencyGraph = jobs
        self.bounding_policy: BoundingPolicy = bounding_policy
        self.w = w

    def branch(self, node: SearchTreeNode) -> list[SearchTreeNode]:
        new_nodes: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()

        candidate: Job
        for candidate in node.candidates:
            new_schedule: list[Job] = [candidate] + node.schedule

            new_candidates: list[Job] = node.candidates
            new_candidates.remove(candidate)

            new_candidates += self.jobs.possible_candidates(new_schedule)

            new_lower_bound: float = self.bounding_policy.bound(
                node, candidate
            )

            new_nodes.put(
                SearchTreeNode(
                    new_schedule,
                    new_candidates,
                    self.jobs,
                    new_lower_bound,
                    node.level + 1,
                )
            )

        return [
            new_nodes.get()
            for _ in range(
                min(self.w(node.level), len(new_nodes.queue))
            )
        ]
