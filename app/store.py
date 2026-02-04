from collections import deque
from dataclasses import dataclass
from time import time
from typing import Deque, Dict, List


@dataclass
class Event:
    ts: float
    ok: bool
    latency_ms: float


class MetricsStore:
    """
    In-memory event store for last N requests.
    Provides summaries for the dashboard.
    """
    def __init__(self, maxlen: int = 5000):
        self.events: Deque[Event] = deque(maxlen=maxlen)

    def add(self, ok: bool, latency_ms: float) -> None:
        self.events.append(Event(ts=time(), ok=ok, latency_ms=latency_ms))

    def snapshot(self, window_sec: int = 300) -> Dict:
        now = time()
        recent: List[Event] = [e for e in self.events if now - e.ts <= window_sec]

        total = len(recent)
        errors = sum(1 for e in recent if not e.ok)

        avg_latency = (sum(e.latency_ms for e in recent) / total) if total else 0.0

        latencies = sorted(e.latency_ms for e in recent)
        if total:
            idx = int(0.95 * (total - 1))
            p95 = latencies[idx]
        else:
            p95 = 0.0

        throughput_rpm = (total / window_sec) * 60 if window_sec > 0 else 0.0

        return {
            "window_sec": window_sec,
            "requests": total,
            "errors": errors,
            "error_rate": (errors / total) if total else 0.0,
            "avg_latency_ms": avg_latency,
            "p95_latency_ms": p95,
            "throughput_rpm": throughput_rpm,
        }

