import logging

from ..bounding_policy.bounding_policy import BoundingPolicy
from ..job_dependencies.graph import Job
from ..job_dependencies.job_dependency_graph import JobDependencyGraph
from ..search_tree.search_tree_node import SearchTreeNode
from .branching_policy import BranchingPolicy


class SingleBranchPolicy(BranchingPolicy):
    def __init__(self, jobs: JobDependencyGraph, bounding_policy: BoundingPolicy):
        logging.info("Using AllBranches Branching Policy")
        self.jobs: JobDependencyGraph = jobs
        self.bounding_policy: BoundingPolicy = bounding_policy

    def branch(self, node: SearchTreeNode) -> list[SearchTreeNode]:
        new_candidates: list[Job] = node.candidates
        candidate = new_candidates[0]
        new_candidates.remove(candidate)

        new_schedule: list[Job] = [candidate] + node.schedule
        new_candidates += self.jobs.possible_candidates(new_schedule)
        new_lower_bound: float = self.bounding_policy.bound(node, candidate)

        return [
            SearchTreeNode(
                new_schedule,
                new_candidates,
                self.jobs,
                new_lower_bound,
                node.level + 1,
            )
        ]
