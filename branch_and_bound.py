from collections import defaultdict

from graph import get_graph, get_node_data
import queue


def get_exit_nodes(N: int, graph: dict[int, list[int]]) -> list[int]:
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


N, graph = get_graph()
processing_times, due_times = get_node_data()

# N = 3
# graph = {0: [1, 2], 1: [], 2: []}
# processing_times = [1, 2, 3]
# due_times = [1, 2, 3]

exit_nodes = get_exit_nodes(N, graph)
inverted_graph = get_inverted_graph(graph)
total_time = sum(processing_times)


class Node:
    def __init__(
        self,
        schedule: list[int],
        candidates: list[int],
        lower_bound: float = 0,
        level: int = 0,
    ):
        self.schedule = schedule
        self.candidates = sorted(candidates)
        self.lower_bound = lower_bound
        self.level = level
        self.schedule_time = sum(map(lambda x: processing_times[x], self.schedule))
        self.terminated = not candidates

    def get_tardiness(self, node: int) -> float:
        end_time = total_time - self.schedule_time
        return max(end_time - due_times[node], 0)

    def branch(self):
        new_nodes: list[Node] = []

        for candidate in self.candidates:
            new_schedule = [candidate] + self.schedule

            new_candidates = self.candidates.copy()
            new_candidates.remove(candidate)

            for graph_candidate in inverted_graph[candidate]:
                children = graph[graph_candidate]
                if all(child in new_schedule for child in children):
                    new_candidates.append(graph_candidate)

            new_lower_bound = self.lower_bound + self.get_tardiness(candidate)

            new_nodes.append(
                Node(new_schedule, new_candidates, new_lower_bound, self.level + 1)
            )

        return new_nodes
    
    def greedy_branch(self) -> "Node":
        best_candidate: int = self.candidates[0]
        best_lower_bound = self.lower_bound + self.get_tardiness(best_candidate)


        for candidate in self.candidates[1:]:
            candidate_lower_bound = self.lower_bound + self.get_tardiness(candidate)
            if candidate_lower_bound < best_lower_bound:
                best_candidate = candidate
                best_lower_bound = candidate_lower_bound

        new_schedule = [best_candidate] + self.schedule
        new_candidates = self.candidates.copy()
        new_candidates.remove(best_candidate)

        for graph_candidate in inverted_graph[best_candidate]:
            children = graph[graph_candidate]
            if all(child in new_schedule for child in children):
                new_candidates.append(graph_candidate)

        return Node(new_schedule, new_candidates, best_lower_bound, self.level + 1)
    

    def __eq__(self, other: "Node") -> bool:  # type: ignore
        return self.lower_bound == other.lower_bound and self.level == other.level

    def __lt__(self, other: "Node") -> bool:
        return (
            self.lower_bound < other.lower_bound
            or (
                self.lower_bound <= other.lower_bound
                and self.terminated
                and not other.terminated
            )
            or (self.lower_bound <= other.lower_bound and self.level > other.level)
        )



def generate_trial_solution(partial_solution: Node) -> Node:
    solution = partial_solution

    while not solution.terminated:
        solution = solution.greedy_branch()

    return solution

nodes = queue.PriorityQueue()
nodes.put(Node([], exit_nodes))

final_schedules = queue.PriorityQueue()
iterations = 0

while not nodes.empty() and iterations < 30000:
    node = nodes.get()

    # Trial solution and achieves the lowest bounded solution
    if node.terminated:
        final_schedules.put(node)
        break

    print(f"Schedule: {node.schedule} Lower Bound: {node.lower_bound}")
    for new_node in node.branch():
        nodes.put(new_node)

        # Adding a terminal nodes to the final solution incase we don't terminate 
        # before the iterations limit
        if new_node.terminated:
            final_schedules.put(new_node)

    iterations += 1

optimal_node = None

if not final_schedules.empty():
    optimal_node = final_schedules.get()
else:
    optimal_node = generate_trial_solution(nodes.get())

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
