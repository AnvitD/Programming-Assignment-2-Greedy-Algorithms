import sys
from collections import deque

def fifo_cache(k: int, requests: list[int]) -> int:
    cache: set[int] = set()
    order: deque[int] = deque()
    misses = 0

    for page in requests:
        if page in cache:
            continue

        misses += 1
        if len(cache) == k:
            evict = order.popleft()
            cache.remove(evict)
        cache.add(page)
        order.append(page)

    return misses
