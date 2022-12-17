SHAPES = (
    (0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j),
    (1 + 0j, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j),
    (0 + 0j, 1 + 0j, 2 + 0j, 2 + 1j, 2 + 2j),
    (0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j),
    (0 + 0j, 0 + 1j, 1 + 0j, 1 + 1j),
)


def fall(chamber, wind_iter, rock):
    while True:
        # Wind blows rock sideways
        wind = next(wind_iter)
        rock_next = [p - 1 if wind == "<" else p + 1 for p in rock]
        if all(0 <= p.real <= 6 and p not in chamber for p in rock_next):
            rock = rock_next

        # Rock falls downwards
        rock_next = [p + complex(0, -1) for p in rock]
        if any(p.imag < 0 or p in chamber for p in rock_next):
            return rock
        rock = rock_next


def cycle(data):
    i = 0
    while True:
        yield data[i]
        i += 1
        if i == len(data):
            i = 0


def run(data):
    chamber = set()
    highest = 0

    shape_iter = cycle(SHAPES)
    wind_iter = cycle(data)

    for _ in range(2022):
        rock = fall(
            chamber,
            wind_iter,
            [p + complex(2, highest + 3) for p in next(shape_iter)],
        )
        chamber.update(rock)
        highest = max(1 + max(p.imag for p in rock), highest)

    return int(highest), 0
