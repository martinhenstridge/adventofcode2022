from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int


HEADINGS = {
    "U": (0, +1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (+1, 0),
}


def parse_motions(data):
    for line in data.splitlines():
        parts = line.split()
        yield HEADINGS[parts[0]], int(parts[1])


def follow(head, tail):
    dx = head.x - tail.x
    dy = head.y - tail.y

    if abs(dx) < 2 and abs(dy) < 2:
        return tail

    cx = max(dx, -1) if dx < 0 else min(dx, 1)
    cy = max(dy, -1) if dy < 0 else min(dy, 1)

    return Position(tail.x + cx, tail.y + cy)


def count_visited(motions, length):
    rope = [Position(0, 0) for _ in range(length)]
    visited = {rope[-1]}

    for (dx, dy), distance in motions:
        for _ in range(distance):
            rope[0] = Position(rope[0].x + dx, rope[0].y + dy)
            for i in range(1, length):
                rope[i] = follow(rope[i - 1], rope[i])
            visited.add(rope[-1])

    return len(visited)


def run(data):
    motions = [m for m in parse_motions(data)]
    return count_visited(motions, 2), count_visited(motions, 10)
