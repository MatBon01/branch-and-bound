import logging
import queue
import sys
from typing import Optional

from utils.bounding_policy.all_others_on_time_policy import AllOthersOnTimePolicy
from utils.bounding_policy.bounding_policy import BoundingPolicy
from utils.branching_policy.all_branches_policy import AllBranchesPolicy
from utils.branching_policy.branching_policy import BranchingPolicy
from utils.job_dependencies.graph import Job, JobGraph, Schedule
from utils.job_dependencies.job_dependency_graph import JobDependencyGraph, get_graph
from utils.search_tree.search_tree_node import SearchTreeNode
from utils.search_tree_explorer.depth_first_search import DepthFirstSearch
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


def generate_solution_using_greedy_depth_first_search(
    jobs: JobDependencyGraph,
    partial_solution: SearchTreeNode,
    brancher: BranchingPolicy,
    current_iteration: int,
) -> tuple[SearchTreeNode, int]:
    logging.info("Generating trial solution from partial solution")
    # Introduce depth first search to go straight to a solution
    # Terminates as soon as a solution is found
    search_tree_explorer: SearchTreeExplorer = DepthFirstSearch(one_depth=True)
    search_tree_explorer.put(partial_solution)

    solution, extra_iterations = branch_and_bound(
        jobs,
        search_tree_explorer,
        brancher,
        initial_nodes=[partial_solution],
        initial_iterations=current_iteration,
        max_iterations=current_iteration + jobs.size,
    )

    return solution, extra_iterations


def branch_and_bound(
    jobs: JobDependencyGraph,
    nodes: SearchTreeExplorer,
    brancher: BranchingPolicy,
    max_iterations: int = 30000,
    initial_iterations: int = 0,
    initial_nodes: list[SearchTreeNode] = None,
) -> tuple[SearchTreeNode, int]:
    if initial_nodes is None:
        nodes.put(SearchTreeNode([], jobs.exit_nodes, jobs))
    else:
        node: SearchTreeNode
        for node in initial_nodes:
            nodes.put(node)

    final_schedules: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
    iteration: int = initial_iterations

    while not nodes.finished() and iteration < max_iterations:
        node, iterations_increment = nodes.next()
        logging.debug("Iteration: %d | %s", iteration, node)

        for new_node in node.branch(brancher):
            # If the node terminates then it is a solution
            if new_node.terminated:
                logging.debug("Found a solution")
                final_schedules.put(new_node)
                nodes.fathom(node.lower_bound)
            else:  # Do not put solutions into nodes
                nodes.put(new_node)

        iteration += iterations_increment

    if not final_schedules.empty():
        optimal_node = final_schedules.get()
    else:
        logging.warning("No final schedules found")
        best_node: SearchTreeNode
        iterations_increment: int = 0
        best_node, iterations_increment = nodes.next()
        iteration += iterations_increment

        optimal_node, iteration = generate_solution_using_greedy_depth_first_search(
            jobs, best_node, brancher, iteration
        )

    return optimal_node, iteration


if __name__ == "__main__":
    main()
