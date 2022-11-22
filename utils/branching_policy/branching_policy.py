from ..search_tree.search_tree_node import SearchTreeNode


class BranchingPolicy:
    def __init__(self):
        pass

    def branch(self, node: SearchTreeNode) -> list[SearchTreeNode]:
        raise NotImplementedError
