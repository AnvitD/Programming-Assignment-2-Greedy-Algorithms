import sys
from collections import deque, OrderedDict

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

def lru_cache(k: int, requests: list[int]) -> int:

    cache: OrderedDict[int, None] = OrderedDict()
    misses = 0

    for page in requests:
        if page in cache:
            cache.move_to_end(page)
            continue

        misses += 1
        if len(cache) == k:
            cache.popitem(last=False)
        cache[page] = None

    return misses

def optff_cache(k: int, requests: list[int]) -> int:

    m = len(requests)
    next_use: list[int] = [m] * m      
    last_seen: dict[int, int] = {}

    for i in range(m - 1, -1, -1):
        page = requests[i]
        if page in last_seen:
            next_use[i] = last_seen[page]
        last_seen[page] = i

    cache: set[int] = set()
    misses = 0

    for i, page in enumerate(requests):
        if page in cache:
            continue 

        misses += 1
        if len(cache) == k:
            victim = max(cache, key=lambda p: _next_occurrence(p, i, requests, m))
            cache.remove(victim)
        cache.add(page)

    return misses


def _next_occurrence(page: int, after: int, requests: list[int], m: int) -> int:
    for j in range(after + 1, m):
        if requests[j] == page:
            return j
    return m

def read_input(path: str) -> tuple[int, list[int]]:
    with open(path) as f:
        first_line = f.readline().split()
        k, m = int(first_line[0]), int(first_line[1])
        requests = list(map(int, f.read().split()))
    if len(requests) != m:
        raise ValueError(
            f"Expected {m} requests but found {len(requests)} in '{path}'."
        )
    return k, requests


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: python {sys.argv[0]} <input_file> [output_file]", file=sys.stderr)
        sys.exit(1)

    k, requests = read_input(sys.argv[1])

    fifo_misses  = fifo_cache (k, requests)
    lru_misses   = lru_cache  (k, requests)
    optff_misses = optff_cache(k, requests)

    lines = [
        f"FIFO  : {fifo_misses}",
        f"LRU   : {lru_misses}",
        f"OPTFF : {optff_misses}",
    ]

    if len(sys.argv) == 3:
        with open(sys.argv[2], "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Output written to {sys.argv[2]}")
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()