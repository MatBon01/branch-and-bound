import queue
from typing import Callable

from utils.bounding_policy.all_others_on_time_policy import AllOthersOnTimePolicy
from utils.bounding_policy.bounding_policy import BoundingPolicy
from utils.branching_policy.all_branches_policy import AllBranchesPolicy
from utils.branching_policy.branching_policy import BranchingPolicy
from utils.branching_policy.greedy_depth_policy import GreedyDepthPolicy
from utils.job_dependencies.graph import Job, JobGraph, Schedule
from utils.job_dependencies.job_dependency_graph import JobDependencyGraph, get_graph
from utils.search_tree.search_tree_node import SearchTreeNode
from utils.search_tree_explorer.jumptracker import JumpTracker
from utils.search_tree_explorer.search_tree_explorer import SearchTreeExplorer


def main():
    jobs: JobDependencyGraph = get_graph()
    explorer: SearchTreeExplorer = JumpTracker()
    bounder: BoundingPolicy = AllOthersOnTimePolicy()
    brancher: BranchingPolicy = AllBranchesPolicy(jobs, bounder)
    optimal_node, iterations = branch_and_bound(jobs, explorer, brancher)

    with open("test.csv", "w") as f:
        f.write(",".join(map(str, optimal_node.schedule)))

    with open("out.txt", "w") as f:
        f.writelines(
            [
                f"Final Schedule = {str(optimal_node.schedule)}\n",
                f"Total tardiness = {optimal_node.lower_bound}\n",
                f"Iterations = {iterations}\n",
            ]
        )


def generate_trial_solution(
    jobs: JobDependencyGraph, partial_solution: SearchTreeNode
) -> SearchTreeNode:
    solution = partial_solution

    greedy_brancher: GreedyDepthPolicy = GreedyDepthPolicy(
        jobs, AllOthersOnTimePolicy()
    )

    print(solution)

    while not solution.terminated:
        solution = solution.branch(greedy_brancher)[0]

    return solution


def branch_and_bound(
    jobs: JobDependencyGraph,
    nodes: SearchTreeExplorer,
    brancher: BranchingPolicy,
    max_iterations: int = 30000,
) -> tuple[SearchTreeNode, int]:
    nodes.put(SearchTreeNode([], jobs.exit_nodes, jobs))

    final_schedules: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
    iterations: int = 0

    while not nodes.finished() and iterations < max_iterations:
        node, iterations_increment = nodes.next()

        # Trial solution and achieves the lowest bounded solution
        if node.terminated:
            final_schedules.put(node)
            break

        print(f"Schedule: {node.schedule} Lower Bound: {node.lower_bound}")
        for new_node in node.branch(brancher):
            nodes.put(new_node)

            # Adding a terminal nodes to the final solution incase we don't terminate
            # before the iterations limit
            if new_node.terminated:
                final_schedules.put(new_node)

        iterations += iterations_increment

    optimal_node = None

    if not final_schedules.empty():
        optimal_node = final_schedules.get()
    else:
        optimal_node = generate_trial_solution(
            jobs, nodes.next()[0]
        )  # TODO:: next might not always be best so maybe extend api

    return optimal_node, iterations


if __name__ == "__main__":
    main()
