def parse_rock_point(point):
    x, y = point.split(",", maxsplit=1)
    return int(x), int(y)


def parse_rock_paths(data):
    return [
        [parse_rock_point(p) for p in line.split(" -> ")] for line in data.splitlines()
    ]


def calculate_step(a, b):
    if a > b:
        return -1
    if a < b:
        return +1
    return 0


def calculate_filled(paths):
    filled = set()

    for path in paths:
        for i in range(len(path) - 1):
            ax, ay = path[i]
            bx, by = path[i + 1]

            dx = calculate_step(ax, bx)
            dy = calculate_step(ay, by)

            x = ax
            y = ay
            while x != bx or y != by:
                filled.add((x, y))
                x += dx
                y += dy
            filled.add((bx, by))

    return filled


def drop_sand(filled, bottom):
    x = 500
    y = 0

    while True:
        if bottom and y > bottom:
            # Fallen into the abyss
            return None

        if (x, y + 1) not in filled:
            y += 1
        elif (x - 1, y + 1) not in filled:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in filled:
            x += 1
            y += 1
        else:
            # Come to rest
            return x, y


def run(data):
    rock_paths = parse_rock_paths(data)
    filled = calculate_filled(rock_paths)

    rocks = len(filled)
    bottom = max(y for _, y in filled)

    while (sand := drop_sand(filled, bottom)) is not None:
        filled.add(sand)
    count1 = len(filled) - rocks

    # Limits found by trial and error
    for x in range(332, 669):
        filled.add((x, bottom + 2))
        rocks += 1

    while (sand := drop_sand(filled, None)) != (500, 0):
        filled.add(sand)
    count2 = 1 + len(filled) - rocks

    return count1, count2
