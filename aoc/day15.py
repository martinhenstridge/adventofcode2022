import re


def parse_sensor_data(data):
    for line in data.splitlines():
        match = re.fullmatch(
            r"Sensor at x=(-?\d+), y=(-?\d+):"
            r" closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        yield (int(match[1]), int(match[2])), (int(match[3]), int(match[4]))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_excluded_spans(sensors, row):
    for position, beacon in sensors:
        along = manhattan(position, beacon) - abs(position[1] - row)
        if along >= 0:
            yield position[0] - along, position[0] + along


def combine_spans(spans):
    ordered = sorted(spans)

    span = ordered.pop(0)
    while ordered:
        other = ordered.pop(0)
        if other[0] <= span[1]:
            span = span[0], max(span[1], other[1])
        else:
            yield span
            span = other
    yield span


def find_excluded_count(sensors, row):
    excluded = tuple(combine_spans(find_excluded_spans(sensors, row)))
    beacons_in_excluded = set(
        beacon
        for _, beacon in sensors
        for span in excluded
        if beacon[1] == row and span[0] <= beacon[0] <= span[1]
    )
    return sum(1 + span[1] - span[0] for span in excluded) - len(beacons_in_excluded)


def find_tuning_frequency(sensors, limit):
    # The solution happens to be nearer the upper bound than the lower,
    # so search backwards to find it faster.
    for row in range(limit, -1, -1):
        excluded = tuple(combine_spans(find_excluded_spans(sensors, row)))
        if len(excluded) > 1:
            return row + 4000000 * (excluded[0][1] + 1)


def run(data):
    sensors = tuple(parse_sensor_data(data))

    excluded_count = find_excluded_count(sensors, 2000000)
    tuning_frequency = find_tuning_frequency(sensors, 4000000)

    return excluded_count, tuning_frequency
