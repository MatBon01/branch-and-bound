import collections
import logging
import queue
import sys
import time
from typing import Optional

from utils.bounding_policy.all_others_on_time_policy import AllOthersOnTimePolicy
from utils.bounding_policy.bounding_policy import BoundingPolicy
from utils.branching_policy.all_branches_policy import AllBranchesPolicy
from utils.branching_policy.beam_search_policy import BeamSearchPolicy
from utils.branching_policy.branching_policy import BranchingPolicy
from utils.job_dependencies.job_dependency_graph import (
    JobDependencyGraph,
    get_graph,
    get_graph_with_fixed_processing_times,
)
from utils.search_tree.search_tree_node import SearchTreeNode
from utils.search_tree_explorer.depth_first_search import DepthFirstSearch
from utils.search_tree_explorer.jumptracker import JumpTracker
from utils.search_tree_explorer.search_tree_explorer import SearchTreeExplorer


def main() -> None:
    setup_logging()
    jobs: JobDependencyGraph = get_graph_with_fixed_processing_times()
    explorer: SearchTreeExplorer = JumpTracker()
    bounder: BoundingPolicy = AllOthersOnTimePolicy()
    brancher: BranchingPolicy = AllBranchesPolicy(jobs, bounder)

    start_time = time.time()
    optimal_node, iterations, max_node_list_size, max_branches = branch_and_bound(
        jobs, explorer, brancher
    )
    end_time = time.time()

    logging.info(f"--- Finished running in {end_time - start_time}s ---")
    logging.info(optimal_node)
    logging.info("Iterations: %d", iterations)
    logging.info("Largest node list size: %d", max_node_list_size)
    logging.info("Max branches: %d", max_branches)


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

    solution, extra_iterations, _, _ = branch_and_bound(
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
    initial_nodes: Optional[list[SearchTreeNode]] = None,
) -> tuple[SearchTreeNode, int, int, int]:
    if initial_nodes is None:
        nodes.put(SearchTreeNode([], jobs.exit_nodes, jobs))
    else:
        node: SearchTreeNode
        for node in initial_nodes:
            nodes.put(node)

    final_schedules: queue.PriorityQueue[SearchTreeNode] = queue.PriorityQueue()
    iteration: int = initial_iterations
    max_node_list_size: int = len(nodes)
    max_branches: int = 0

    while not nodes.finished() and iteration < max_iterations:
        node, iterations_increment = nodes.next()
        logging.debug("Iteration: %d | %s", iteration, node)

        new_nodes = node.branch(brancher)

        for new_node in new_nodes:
            # If the node terminates then it is a solution
            if new_node.terminated:
                logging.debug("Found a solution")
                final_schedules.put(new_node)
                nodes.fathom(node.lower_bound)
            else:  # Do not put solutions into nodes
                nodes.put(new_node)

        iteration += iterations_increment

        max_node_list_size = max(max_node_list_size, len(nodes))
        max_branches = max(max_branches, len(new_nodes))

    if not final_schedules.empty():
        optimal_node = final_schedules.get()
    else:
        logging.warning("No final schedules found")
        optimal_node, iteration = generate_solution_using_greedy_depth_first_search(
            jobs, nodes.best(), brancher, iteration
        )

    return optimal_node, iteration, max_node_list_size, max_branches


if __name__ == "__main__":
    main()
