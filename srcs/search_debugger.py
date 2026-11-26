from dataclasses import dataclass
from time import perf_counter


@dataclass(frozen=True)
class SearchStats:
    nodes: int = 0
    elapsed_time: float = 0.0
    pruning_count: int = 0
    best_score: float | None = None
    completed_depth: int = 0


class SearchDebugger:
    def __init__(self) -> None:
        self.start()

    def start(self) -> None:
        self._started = perf_counter()
        self._nodes = 0
        self._pruning_count = 0
        self._best_score = None
        self._completed_depth = 0
        self._elapsed_time = 0.0

    def record_node(self) -> None:
        self._nodes += 1

    def record_pruning(self) -> None:
        self._pruning_count += 1

    def record_result(self, score: float, depth: int) -> None:
        self._best_score = score
        self._completed_depth = depth

    def finish(self) -> None:
        self._elapsed_time = perf_counter() - self._started

    def get_stats(self) -> SearchStats:
        return SearchStats(
            nodes=self._nodes,
            elapsed_time=self._elapsed_time,
            pruning_count=self._pruning_count,
            best_score=self._best_score,
            completed_depth=self._completed_depth,
        )

    def print_stats(self) -> None:
        stats = self.get_stats()

        print(f"Nodes: {stats.nodes}")
        print(f"Elapsed time: {stats.elapsed_time * 1000:.2f} ms")
        print(f"Cutoffs: {stats.pruning_count}")
        print(f"Best score: {stats.best_score}")
        print(f"Completed depth: {stats.completed_depth}")
