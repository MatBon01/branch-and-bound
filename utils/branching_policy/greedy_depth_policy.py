from ..bounding_policy.bounding_policy import BoundingPolicy
from ..job_dependencies.graph import Job
from ..job_dependencies.job_dependency_graph import JobDependencyGraph
from ..search_tree.search_tree_node import SearchTreeNode
from .branching_policy import BranchingPolicy


class GreedyDepthPolicy(BranchingPolicy):
    def __init__(self, jobs: JobDependencyGraph, bounding_policy: BoundingPolicy):
        self.jobs: JobDependencyGraph = jobs
        self.bounding_policy: BoundingPolicy = bounding_policy

    def branch(self, node: SearchTreeNode) -> list[SearchTreeNode]:
        best_candidate: Job = node.candidates[0]
        best_lower_bound: float = self.bounding_policy.bound(node, best_candidate)

        candidate: Job
        for candidate in node.candidates[1:]:
            candidate_lower_bound: float = self.bounding_policy.bound(node, candidate)
            if candidate_lower_bound < best_lower_bound:
                best_candidate = candidate
                best_lower_bound = candidate_lower_bound

        new_schedule: list[Job] = [best_candidate] + node.schedule
        new_candidates: list[Job] = node.candidates
        new_candidates.remove(best_candidate)

        new_candidates += self.jobs.possible_candidates(new_schedule)

        return [
            SearchTreeNode(
                new_schedule,
                new_candidates,
                self.jobs,
                best_lower_bound,
                node.level + 1,
            )
        ]
