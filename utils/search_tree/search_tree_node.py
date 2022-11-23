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

    def get_tardiness(self, job: Job) -> float:
        end_time = self._jobs.total_time - self._schedule_time
        return max(end_time - self._jobs[job].due_time, 0)

    def branch(self, brancher) -> list["SearchTreeNode"]:
        return brancher.branch(self)

    def __eq__(self, other: "SearchTreeNode") -> bool:  # type: ignore
        return self.lower_bound == other.lower_bound and self.level == other.level

    def __lt__(self, other: "SearchTreeNode") -> bool:
        return (
            self.lower_bound < other.lower_bound
            or (
                self.lower_bound <= other.lower_bound
                and self.terminated
                and not other.terminated
            )
            or (self.lower_bound <= other.lower_bound and self._level > other._level)
        )

    @property
    def schedule_as_string(self) -> str:
        return ",".join(map(str, self.schedule))

    def __str__(self) -> str:
        return f"Reverse schedule: {self.schedule_as_string} | Lower bound: {self.lower_bound}"

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
        return not self._candidates

    @property
    def level(self) -> int:
        return self._level
