import math
import itertools

MOVES = (
    (0, 0),  # wait
    (0, -1),  # up
    (0, +1),  # down
    (-1, 0),  # left
    (+1, 0),  # right
)


def parse_initial_state(data):
    lines = data.splitlines()

    start = lines[0].find("."), 0
    finish = lines[-1].find("."), len(lines) - 1

    walls = []
    blizzards = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                walls.append((x, y))
            elif char != ".":
                blizzards.append((char, x, y))

    return start, finish, walls, blizzards


def lcm(a, b):
    # There's no stdlib lcm function until python 3.9.
    return a * b // math.gcd(a, b)


def advance_blizzards(blizzards, xmax, ymax):
    advanced = []

    for which, x, y in blizzards:
        if which == "^":
            y -= 1
            if y == 0:
                y = ymax - 1
        elif which == "v":
            y += 1
            if y == ymax:
                y = 1
        elif which == "<":
            x -= 1
            if x == 0:
                x = xmax - 1
        elif which == ">":
            x += 1
            if x == xmax:
                x = 1
        advanced.append((which, x, y))

    return advanced


def calculate_obstacle_series(walls, blizzards):
    xmax = max(x for x, y in walls)
    ymax = max(y for x, y in walls)

    # Add extra walls at top and bottom to prevent going out-of-bounds
    # from the start or finish.
    for x in range(xmax + 1):
        walls.append((x, -1))
        walls.append((x, ymax + 1))

    # The <> blizzards repeat with a period that matches the width of
    # the valley. Similarly the ^v blizzards repeat with a period that
    # matches the height of the valley. Their combined period is the
    # least common multiple of the <> and ^v periods.
    period = lcm(xmax - 1, ymax - 1)

    # Calculate obstacle (i.e. wall or blizzard) locations throughout
    # the calculated period.
    obstacle_series = []
    for _ in range(period):
        obstacles = set(walls)
        for _, x, y in blizzards:
            obstacles.add((x, y))
        obstacle_series.append(obstacles)
        blizzards = advance_blizzards(blizzards, xmax, ymax)

    # Finally, cycle through the pre-calculated obstacle locations.
    i = 0
    while True:
        yield obstacle_series[i]
        i += 1
        if i == period:
            i = 0


def search(start, goal, obstacle_series, t0):
    elves = set()
    elves.add(start)

    for t in itertools.count(start=t0):
        obstacles = next(obstacle_series)
        elves_next = set()

        for x, y in elves:
            for dx, dy in MOVES:
                p = (x + dx, y + dy)
                if p not in obstacles:
                    elves_next.add(p)
                if p == goal:
                    return t

        elves = elves_next


def run(data):
    start, finish, walls, blizzards = parse_initial_state(data)
    obstacle_series = calculate_obstacle_series(walls, blizzards)

    t1 = search(start, finish, obstacle_series, t0=0)
    t2 = search(finish, start, obstacle_series, t0=t1 + 1)
    t3 = search(start, finish, obstacle_series, t0=t2 + 1)

    return t1, t3
