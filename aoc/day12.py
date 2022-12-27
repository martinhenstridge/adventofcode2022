import math
import heapq
import collections


def parse_heightmap(data):
    grid = {}
    start = None
    end = None

    lines = data.splitlines()
    for y, line in enumerate(lines):
        for x, height in enumerate(line):
            if height == "S":
                start = (x, y)
                height = "a"
            elif height == "E":
                end = (x, y)
                height = "z"
            grid[x, y] = ord(height)

    return grid, start, end


def find_candidates(grid, position):
    x, y = position
    h = grid[position]
    candidates = []

    for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
        cp = x + dx, y + dy

        # Ignore candidate squares outside the grid.
        try:
            ch = grid[cp]
        except KeyError:
            continue

        # Ignore candidate squares which are inaccessible from the
        # current position.
        if ch > h + 1:
            continue

        # Ignore the option of moving from one 'a' square to another.
        # Starting from the latter will always result in a shorter path,
        # and it's possible to move from S directly to a 'b' square.
        if h == ord("a") and h == ch:
            continue

        # The candidate square is acceptable, store it.
        candidates.append(cp)

    return candidates


def find_shortest_path(candidates, end, start):
    fewest = collections.defaultdict(lambda: math.inf)
    fewest[start] = 0

    pending = []
    heapq.heappush(pending, (0, start))

    while pending:
        _, p = heapq.heappop(pending)
        if p == end:
            return fewest[end]

        for c in candidates[p]:
            distance = fewest[p] + 1
            if distance < fewest[c]:
                fewest[c] = distance
                heapq.heappush(pending, (distance, c))

    return math.inf


def run(data):
    grid, start, end = parse_heightmap(data)
    candidates = {p: find_candidates(grid, p) for p in grid}

    from_start = find_shortest_path(candidates, end, start)
    from_any_a = min(
        find_shortest_path(candidates, end, p) for p, h in grid.items() if h == ord("a")
    )

    return from_start, from_any_a
