import itertools

# Coordinates of rock parts: real is x, imaginary is y.
SHAPES = (
    (0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j),
    (1 + 0j, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j),
    (0 + 0j, 1 + 0j, 2 + 0j, 2 + 1j, 2 + 2j),
    (0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j),
    (0 + 0j, 0 + 1j, 1 + 0j, 1 + 1j),
)


def simulate(chamber, highest, wind_iter, shape_iter):
    rock = [p + complex(2, highest + 3) for p in next(shape_iter)]

    while True:
        wind = next(wind_iter)
        rock_next = [p - 1 if wind == "<" else p + 1 for p in rock]
        if all(0 <= p.real <= 6 and p not in chamber for p in rock_next):
            rock = rock_next

        rock_next = [p - 1j for p in rock]
        if any(p.imag < 0 or p in chamber for p in rock_next):
            break
        rock = rock_next

    chamber.update(rock)
    highest = max(1 + max(p.imag for p in rock), highest)

    return chamber, highest


def calculate_height(history, offset, period, iterations):
    loops = (iterations - offset) // period
    index = (iterations - offset) - (loops * period)
    return history[index] + loops * (history[-1] - history[0])


def run(data):
    chamber = set()
    highest = 0

    wind_iter = itertools.cycle(data)
    shape_iter = itertools.cycle(SHAPES)

    # From experimentation, the simulation loops exactly in sync with
    # the air jets. The first loop takes 1728 rocks and then each
    # subsequent loop takes 1735 rocks (assuming the difference here is
    # due to the initial loop starting from a completely flat floor and
    # subsequent loops starting from some other conformation).
    offset = 1728
    period = 1735

    # Reach beginning of cycle
    for _ in range(offset):
        chamber, highest = simulate(chamber, highest, wind_iter, shape_iter)

    # Run through a complete cycle, collecting height history
    history = []
    for _ in range(period):
        chamber, highest = simulate(chamber, highest, wind_iter, shape_iter)
        history.append(int(highest))

    # Extrapolate height for the requested rock counts.
    part1 = calculate_height(history, offset, period, 2022 - 1)
    part2 = calculate_height(history, offset, period, 1000000000000 - 1)

    return part1, part2
