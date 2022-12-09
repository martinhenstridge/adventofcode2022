HEADINGS = {
    "U": complex(0, +1),
    "D": complex(0, -1),
    "L": complex(-1, 0),
    "R": complex(+1, 0),
}


def parse_motions(data):
    for line in data.splitlines():
        parts = line.split()
        yield HEADINGS[parts[0]], int(parts[1])


def follow(head, tail):
    dp = head - tail

    if abs(dp.real) > 1 or abs(dp.imag) > 1:
        real = max(dp.real, -1) if dp.real < 0 else min(dp.real, +1)
        imag = max(dp.imag, -1) if dp.imag < 0 else min(dp.imag, +1)
        tail += complex(real, imag)

    return tail


def count_visited(motions, length):
    rope = [complex(0, 0) for _ in range(length)]
    visited = {rope[-1]}

    for heading, distance in motions:
        for _ in range(distance):
            rope[0] = rope[0] + heading
            for i in range(1, length):
                rope[i] = follow(rope[i - 1], rope[i])
            visited.add(rope[-1])

    return len(visited)


def run(data):
    motions = [m for m in parse_motions(data)]
    return count_visited(motions, 2), count_visited(motions, 10)
