from ..search_tree.search_tree_node import SearchTreeNode


class SearchTreeExplorer:
    def __init__(self):
        pass

    def put(self, node: SearchTreeNode) -> None:
        pass

    def next(self) -> tuple[SearchTreeNode, int]:  # second int is iterations increment
        pass

    def finished(self) -> bool:
        pass

    def fathom(self, solution_time: int) -> None:
        pass

    def best(self) -> SearchTreeNode:
        pass

    def __len__(self) -> int:
        return 0
