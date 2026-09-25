from collections import deque
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Sample:
    key: str
    value: float
    timestamp: float

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("sample key is required")
        if not math.isfinite(self.value) or not math.isfinite(self.timestamp):
            raise ValueError("sample value and timestamp must be finite")


class Window:
    def __init__(self, size_s: float, max_samples: int = 10_000) -> None:
        if not math.isfinite(size_s) or size_s <= 0:
            raise ValueError("window size must be positive and finite")
        if max_samples < 1:
            raise ValueError("max_samples must be positive")
        self.size_s = size_s
        self.max_samples = max_samples
        self._q: deque[Sample] = deque()

    def add(self, sample: Sample) -> None:
        if self._q and sample.timestamp < self._q[-1].timestamp:
            raise ValueError("out-of-order sample")
        self._q.append(sample)
        if len(self._q) > self.max_samples:
            raise OverflowError("window capacity exceeded")
        self._evict(sample.timestamp)

    def _evict(self, now: float) -> None:
        while self._q and now - self._q[0].timestamp > self.size_s:
            self._q.popleft()

    def aggregate(self, key: str) -> float:
        if not key.strip():
            raise ValueError("aggregation key is required")
        values = [sample.value for sample in self._q if sample.key == key]
        return sum(values) / len(values) if values else 0.0

    def __len__(self) -> int:
        return len(self._q)
