import logging
import queue
import sys

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


def main() -> None:
    setup_logging()
    jobs: JobDependencyGraph = get_graph()
    explorer: SearchTreeExplorer = JumpTracker()
    bounder: BoundingPolicy = AllOthersOnTimePolicy()
    brancher: BranchingPolicy = AllBranchesPolicy(jobs, bounder)
    optimal_node, iterations = branch_and_bound(jobs, explorer, brancher)

    logging.info("---FINISHED---")
    logging.info(optimal_node)
    logging.info("Iterations: %d", iterations)


def setup_logging(
    log_name: str = "bbschedule.log", format: str = "%(message)s"
) -> None:
    print_info: logging.Handler = logging.StreamHandler(sys.stdout)
    print_info.setLevel(logging.INFO)

    file_log: logging.Handler = logging.FileHandler(log_name)
    file_log.setLevel(logging.DEBUG)

    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG,
        format=format,
        handlers=[print_info, file_log],
    )


def generate_trial_solution(
    jobs: JobDependencyGraph, partial_solution: SearchTreeNode
) -> SearchTreeNode:
    logging.info("Generating trial solution from partial solution")
    solution = partial_solution

    greedy_brancher: GreedyDepthPolicy = GreedyDepthPolicy(
        jobs, AllOthersOnTimePolicy()
    )

    while not solution.terminated:
        logging.debug(solution)
        solution = solution.branch(greedy_brancher)[0]

    logging.debug(solution)

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

        logging.debug(node)
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
        logging.warning("No final schedules found")
        optimal_node = generate_trial_solution(
            jobs, nodes.next()[0]
        )  # TODO:: next might not always be best so maybe extend api

    return optimal_node, iterations


if __name__ == "__main__":
    main()
