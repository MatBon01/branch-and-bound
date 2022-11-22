from collections import defaultdict

from utils.job_dependencies.graph import Job
from utils.job_dependencies.job_dependency_graph import JobDependencyGraph, get_graph


def main():
    jobs: JobDependencyGraph = get_graph()
    print(hu_algorithm(jobs))


def hu_algorithm(jobs: JobDependencyGraph) -> list[Job]:
    node_levels: dict[Job, int] = {node: 1 for node in jobs.exit_nodes}
    schedule: list[Job] = []

    current_level: int = 1
    current_level_nodes: list[Job] = list(jobs.exit_nodes)

    while current_level_nodes:
        new_level_nodes: list[Job] = []

        node: Job
        for node in current_level_nodes:
            parent: Job
            for parent in jobs[node].dependencies:
                node_levels[parent] = current_level + 1
                new_level_nodes.append(parent)

        current_level_nodes = new_level_nodes
        current_level += 1

    level_nodes: dict[int, list[Job]] = defaultdict(list)

    node: Job
    level: int
    for node, level in node_levels.items():
        level_nodes[level].append(node)

    level: int
    for level in range(max(node_levels.values()), 0, -1):
        schedule += sorted(level_nodes[level])

    return schedule


if __name__ == "__main__":
    main()
