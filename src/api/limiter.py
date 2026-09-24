"""
Sliding Window Rate Limiter for LLM & API Protection
"""

import time
import asyncio
import threading
from typing import Dict, List, Tuple
from collections import OrderedDict


class SlidingWindowRateLimiter:
    """Thread-safe sliding window limiter with cleanup and async support."""
    def __init__(self, requests_per_minute: int = 30, max_clients: int = 5000):
        self.rate = requests_per_minute
        self.window = 60.0
        self.max_clients = max_clients
        self.clients: Dict[str, List[float]] = OrderedDict()
        self._lock = threading.Lock()
        self._async_lock = asyncio.Lock()

    def _prune(self, now: float):
        # Remove stale clients to prevent unbounded growth
        to_delete = []
        for cid, hist in self.clients.items():
            if not hist or (now - hist[-1] > self.window * 2):
                to_delete.append(cid)
            if len(to_delete) > 100:
                break
        for cid in to_delete:
            self.clients.pop(cid, None)
        # Enforce max_clients LRU eviction
        while len(self.clients) > self.max_clients:
            self.clients.popitem(last=False)

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        now = time.time()
        with self._lock:
            history = self.clients.get(client_id, [])
            history = [t for t in history if now - t < self.window]
            if len(history) >= self.rate:
                self.clients[client_id] = history
                self._prune(now)
                retry_after = int(self.window - (now - history[0])) + 1
                return False, max(1, retry_after)
            history.append(now)
            self.clients[client_id] = history
            self._prune(now)
            return True, 0

    async def is_allowed_async(self, client_id: str) -> Tuple[bool, int]:
        # asyncio-safe wrapper
        async with self._async_lock:
            return self.is_allowed(client_id)


# Global singleton to avoid dual instances
_global_limiter: SlidingWindowRateLimiter | None = None

def get_global_limiter(requests_per_minute: int = 30) -> SlidingWindowRateLimiter:
    global _global_limiter
    if _global_limiter is None:
        _global_limiter = SlidingWindowRateLimiter(requests_per_minute=requests_per_minute)
    return _global_limiter
