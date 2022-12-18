import math


def parse_cubes(data):
    for line in data.splitlines():
        yield tuple(int(part) for part in line.split(","))


def get_neighbours(p):
    x, y, z = p
    return (
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    )


def calculate_surface_area(cubes):
    return sum(
        0 if neighbour in cubes else 1
        for cube in cubes
        for neighbour in get_neighbours(cube)
    )


def calculate_external_area(cubes):
    xmin = math.inf
    ymin = math.inf
    zmin = math.inf
    xmax = -math.inf
    ymax = -math.inf
    zmax = -math.inf

    for x, y, z in cubes:
        if x < xmin:
            xmin = x
        if y < ymin:
            ymin = y
        if z < zmin:
            zmin = z
        if x > xmax:
            xmax = x
        if y > ymax:
            ymax = y
        if z > zmax:
            zmax = z

    # Expand min/max by 1 in each direction to allow search to move
    # around the outside extreme points.
    xmin -= 1
    ymin -= 1
    zmin -= 1
    xmax += 1
    ymax += 1
    zmax += 1

    # Visit all reachable points starting from an arbitrary point known
    # to reside outside of the shape, keeping track of the number of
    # neighbouring lava cubes for each. The sum of these counts is the
    # external area of the shape.
    visited = {}
    candidates = [(xmin, ymin, zmin)]

    while candidates:
        candidate = candidates.pop()
        count = 0

        for neighbour in get_neighbours(candidate):
            # Avoid visiting anywhere twice.
            if neighbour in visited:
                continue

            # This neighbour is part of the external surface.
            if neighbour in cubes:
                count += 1
                continue

            # Bounds check before adding neighbour to search candidates.
            nx, ny, nz = neighbour
            if nx < xmin or nx > xmax:
                continue
            if ny < ymin or ny > ymax:
                continue
            if nz < zmin or nz > zmax:
                continue
            candidates.append(neighbour)

        visited[candidate] = count

    return sum(visited.values())


def run(data):
    cubes = set(parse_cubes(data))

    surface_area = calculate_surface_area(cubes)
    external_area = calculate_external_area(cubes)

    return surface_area, external_area
