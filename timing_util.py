import dataclasses
from time import perf_counter_ns as timestamp_nano


@dataclasses.dataclass(slots=True)
class Timing:
    message: str = "Elapsed time: "
    start: int = dataclasses.field(init=False)

    def __enter__(self) -> None:
        self.start = timestamp_nano()

    def __exit__(self, type, value, traceback) -> None:
        diff = timestamp_nano() - self.start
        if diff < 1e3:
            print(f"{self.message}{diff:.3f}ns")
        elif diff < 1e6:
            print(f"{self.message}{diff / 1e3:.3f}µs")
        elif diff < 1e9:
            print(f"{self.message}{diff / 1e6:.3f}ms")
        else:
            print(f"{self.message}{diff / 1e9:.3f}s")
