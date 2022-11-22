from collections import defaultdict

from .graph import Job, N, due_times, links, processing_times


def get_legacy_graph() -> tuple[int, dict[Job, list[Job]]]:
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in links:
        graph[u].append(v)

    return N, graph


def get_node_data() -> tuple[list[float], list[int]]:
    return processing_times, due_times


def legacy_get_exit_nodes(N: int, graph: dict[int, list[int]]) -> list[int]:
    exit_nodes: list[int] = []
    for node in range(N):
        if not graph[node]:
            exit_nodes.append(node)

    return exit_nodes


def get_inverted_graph(graph: dict[int, list[int]]) -> dict[int, list[int]]:
    inverted_graph: dict[int, list[int]] = defaultdict(list)
    for node, children in graph.items():
        for child in children:
            inverted_graph[child].append(node)

    return inverted_graph
