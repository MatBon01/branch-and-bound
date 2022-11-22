import logging

from ..bounding_policy.bounding_policy import BoundingPolicy
from ..job_dependencies.graph import Job
from ..job_dependencies.job_dependency_graph import JobDependencyGraph
from ..search_tree.search_tree_node import SearchTreeNode
from .branching_policy import BranchingPolicy


class AllBranchesPolicy(BranchingPolicy):
    def __init__(self, jobs: JobDependencyGraph, bounding_policy: BoundingPolicy):
        logging.info("Using AllBranches Branching Policy")
        self.jobs: JobDependencyGraph = jobs
        self.bounding_policy: BoundingPolicy = bounding_policy

    def branch(self, search_tree_node: SearchTreeNode) -> list[SearchTreeNode]:
        new_nodes: list[SearchTreeNode] = []

        candidate: Job
        for candidate in search_tree_node.candidates:
            new_schedule: list[Job] = [candidate] + search_tree_node.schedule

            new_candidates: list[Job] = search_tree_node.candidates
            new_candidates.remove(candidate)

            new_candidates += self.jobs.possible_candidates(new_schedule)

            new_lower_bound: float = self.bounding_policy.bound(
                search_tree_node, candidate
            )

            new_nodes.append(
                SearchTreeNode(
                    new_schedule,
                    new_candidates,
                    self.jobs,
                    new_lower_bound,
                    search_tree_node.level + 1,
                )
            )

        return new_nodes
