from ..job_dependencies.graph import Job
from ..search_tree.search_tree_node import SearchTreeNode


class BoundingPolicy:
    def __init__(self):
        pass

    def bound(self, current_node: SearchTreeNode, candidate_job: Job) -> float:
        pass
