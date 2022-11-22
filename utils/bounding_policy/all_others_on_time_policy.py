import logging

from ..job_dependencies.graph import Job
from ..search_tree.search_tree_node import SearchTreeNode
from .bounding_policy import BoundingPolicy


class AllOthersOnTimePolicy(BoundingPolicy):
    def __init__(self):
        logging.info("Using AllOthersOnTime Bounding Policy")

    def bound(self, current_node: SearchTreeNode, candidate_job: Job) -> float:
        return current_node.lower_bound + current_node.get_tardiness(candidate_job)
