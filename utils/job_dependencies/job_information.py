from .graph import Job


class JobInformation:
    def __init__(
        self,
        processing_time: int,
        due_time: int,
        dependents: list[Job],
        dependencies: list[Job],
    ):
        self._processing_time: int = processing_time
        self._due_time: int = due_time
        self._dependents: list[Job] = dependents
        self._dependencies: list[Job] = dependencies

    @property
    def dependents(self) -> list[Job]:
        return self._dependents

    @property
    def dependencies(self) -> list[Job]:
        return self._dependencies

    @property
    def processing_time(self) -> int:
        return self._processing_time

    @property
    def due_time(self) -> int:
        return self._due_time
