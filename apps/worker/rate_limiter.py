import asyncio
import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class RateLimitResult:
    allowed: bool
    wait_time: float


class TokenBucket:
    def __init__(self, rate_per_minute: int):
        self.capacity = rate_per_minute
        self.tokens = rate_per_minute
        self.refill_rate = rate_per_minute / 60.0
        self.last_check = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> RateLimitResult:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_check
            self.last_check = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            if self.tokens >= 1:
                self.tokens -= 1
                return RateLimitResult(True, 0.0)
            wait_time = (1 - self.tokens) / self.refill_rate
            return RateLimitResult(False, wait_time)


async def with_retry(
    func: Callable,
    *args,
    retries: int = 3,
    backoff: float = 0.5,
    **kwargs,
):
    attempt = 0
    while True:
        try:
            return await func(*args, **kwargs)
        except Exception:
            attempt += 1
            if attempt > retries:
                raise
            await asyncio.sleep(backoff * attempt)
