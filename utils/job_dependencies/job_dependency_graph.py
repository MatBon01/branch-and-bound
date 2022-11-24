from collections import defaultdict

from .graph import Job, due_times, links, processing_times, fixed_processing_times
from .graph_utils import get_inverted_graph
from .job_information import JobInformation


class JobDependencyGraph:
    def __init__(
        self,
        edges: list[list[tuple[Job, Job]]],
        processing_times: list[float],
        due_times: list[int],
    ):
        self.dependencies: dict[Job, list[Job]] = defaultdict(list)
        job: Job
        dependent_jobs: list[Job]
        for job, dependent_jobs in edges:
            self.dependencies[job].append(dependent_jobs)

        self.inverted_dependencies: dict[Job, list[Job]] = get_inverted_graph(
            self.dependencies
        )
        self.processing_times: list[float] = processing_times
        self.due_times: list[int] = due_times
        self.jobs_information: dict[Job, JobInformation] = {}

    def __getitem__(self, job: Job) -> JobInformation:
        if job in self.jobs_information:
            return self.jobs_information[job]
        else:
            self.jobs_information[job] = JobInformation(
                self.processing_times[job],
                self.due_times[job],
                self.dependencies[job],
                self.inverted_dependencies[job],
            )
            return self.jobs_information[job]

    def possible_candidates(self, partial_schedule: list[Job]) -> list[Job]:
        possible_candidates: list[Job] = []
        # The dependencies of the candidate job are the only new jobs
        # that can now be scheduled
        graph_candidate: Job
        for graph_candidate in self[partial_schedule[0]].dependencies:
            # Check all dependents are in the (reversed) schedule so they
            # cannot be scheduled before their dependency
            children: list[Job] = self[graph_candidate].dependents
            if all(child in partial_schedule for child in children):
                possible_candidates.append(graph_candidate)

        return possible_candidates

    @property
    def size(self) -> int:
        return len(self.processing_times)

    @property
    def exit_nodes(self) -> list[Job]:
        exit_nodes: list[Job] = []
        for node in range(self.size):
            if not self.dependencies[node]:
                exit_nodes.append(node)

        return exit_nodes

    @property
    def total_time(self) -> float:
        return sum(self.processing_times)


def get_graph() -> JobDependencyGraph:
    return JobDependencyGraph(links, processing_times, due_times)


def get_graph_with_fixed_processing_times() -> JobDependencyGraph:
    return JobDependencyGraph(links, fixed_processing_times, due_times)