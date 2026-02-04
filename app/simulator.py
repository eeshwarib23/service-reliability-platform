import random
import time
from dataclasses import dataclass


@dataclass
class SimConfig:
    base_latency_ms: int = 80
    jitter_ms: int = 120
    error_rate: float = 0.05  # 5% errors


def handle_request(cfg: SimConfig) -> tuple[bool, float]:
    """
    Simulate backend work. Returns (ok, latency_ms).
    """
    start = time.perf_counter()

    sleep_ms = cfg.base_latency_ms + random.randint(0, cfg.jitter_ms)
    time.sleep(sleep_ms / 1000.0)

    ok = random.random() >= cfg.error_rate
    latency_ms = (time.perf_counter() - start) * 1000.0
    return ok, latency_ms
