import enum
import math
import itertools
import collections


class Direction(enum.Flag):
    NONE = 0
    N = 0x1
    S = 0x2
    W = 0x4
    E = 0x8
    NW = 0x10
    NE = 0x20
    SW = 0x40
    SE = 0x80


def parse_elves(data):
    elves = set()
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                elves.add((x, y))
    return elves


def find_neighbours(elves, x, y):
    neighbours = Direction.NONE

    if (x, y - 1) in elves:
        neighbours |= Direction.N
    if (x, y + 1) in elves:
        neighbours |= Direction.S
    if (x - 1, y) in elves:
        neighbours |= Direction.W
    if (x + 1, y) in elves:
        neighbours |= Direction.E
    if (x - 1, y - 1) in elves:
        neighbours |= Direction.NW
    if (x + 1, y - 1) in elves:
        neighbours |= Direction.NE
    if (x - 1, y + 1) in elves:
        neighbours |= Direction.SW
    if (x + 1, y + 1) in elves:
        neighbours |= Direction.SE

    return neighbours


def run_round(elves, directions):
    movement = False
    proposed_moves = collections.defaultdict(list)

    # First half: propose a move.
    for elf in elves:
        x, y = elf
        neighbours = find_neighbours(elves, x, y)

        # No neighbours, elf doesn't move.
        if neighbours is Direction.NONE:
            continue

        # Work out which direction to move.
        for direction, (bitmask, dx, dy) in directions.items():
            if neighbours & bitmask is Direction.NONE:
                proposed_moves[x + dx, y + dy].append(elf)
                break

    # Second half: attempt to move.
    for move, movers in proposed_moves.items():
        if len(movers) == 1:
            movement = True
            elves.remove(movers[0])
            elves.add(move)

    # Rotate the directions, move first element to the end.
    d = next(iter(directions))
    directions[d] = directions.pop(d)

    return movement


def count_empty_tiles(elves):
    xmin = math.inf
    ymin = math.inf
    xmax = -math.inf
    ymax = -math.inf

    for x, y in elves:
        xmin = min(xmin, x)
        ymin = min(ymin, y)
        xmax = max(xmax, x)
        ymax = max(ymax, y)

    return (1 + xmax - xmin) * (1 + ymax - ymin) - len(elves)


def run(data):
    elves = parse_elves(data)

    directions = {
        Direction.N: (Direction.N | Direction.NE | Direction.NW, 0, -1),
        Direction.S: (Direction.S | Direction.SE | Direction.SW, 0, +1),
        Direction.W: (Direction.W | Direction.NW | Direction.SW, -1, 0),
        Direction.E: (Direction.E | Direction.NE | Direction.SE, +1, 0),
    }

    for round_number in itertools.count(start=1):
        movement = run_round(elves, directions)
        if round_number == 10:
            empty_tiles = count_empty_tiles(elves)
        if not movement:
            break

    return empty_tiles, round_number
