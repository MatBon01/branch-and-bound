from ..job_dependencies.graph import Job
from ..job_dependencies.job_dependency_graph import JobDependencyGraph


class SearchTreeNode:
    def __init__(
        self,
        schedule: list[Job],
        candidates: list[Job],
        jobs: JobDependencyGraph,
        lower_bound: float = 0,
        level: int = 0,
    ):
        self._schedule: list[Job] = schedule
        self._candidates: list[Job] = sorted(candidates)
        self._jobs: JobDependencyGraph = jobs
        self._lower_bound: float = lower_bound
        self._level: int = level
        self._schedule_time: int = sum(
            map(lambda x: self._jobs[x].processing_time, self._schedule)
        )
        self._terminated: bool = not candidates

    def get_tardiness(self, job: Job) -> float:
        end_time = self._jobs.total_time - self._schedule_time
        return max(end_time - self._jobs[job].due_time, 0)

    def branch(self, brancher) -> list["SearchTreeNode"]:
        return brancher.branch(self)

    def __eq__(self, other: "SearchTreeNode") -> bool:  # type: ignore
        return self.lower_bound == other.lower_bound and self._level == other._level

    def __lt__(self, other: "SearchTreeNode") -> bool:
        return (
            self.lower_bound < other.lower_bound
            or (
                self.lower_bound <= other.lower_bound
                and self._terminated
                and not other._terminated
            )
            or (self.lower_bound <= other.lower_bound and self._level > other._level)
        )

    @property
    def candidates(self) -> list[Job]:
        return self._candidates.copy()

    @property
    def schedule(self) -> list[Job]:
        return self._schedule

    @property
    def lower_bound(self) -> float:
        return self._lower_bound

    @property
    def terminated(self) -> bool:
        return self._terminated

    @property
    def level(self) -> int:
        return self._level
