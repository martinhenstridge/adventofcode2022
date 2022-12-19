import re


def parse_blueprint_ident(s):
    match = re.match(r"Blueprint (\d+):", s)
    return int(match[1])


def parse_cost_ore_robot(s):
    match = re.search(r"Each ore robot costs (\d+) ore.", s)
    return (int(match[1]), 0, 0, 0)


def parse_cost_clay_robot(s):
    match = re.search(r"Each clay robot costs (\d+) ore.", s)
    return (int(match[1]), 0, 0, 0)


def parse_cost_obsidian_robot(s):
    match = re.search(r"Each obsidian robot costs (\d+) ore and (\d+) clay.", s)
    return (int(match[1]), int(match[2]), 0, 0)


def parse_cost_geode_robot(s):
    match = re.search(r"Each geode robot costs (\d+) ore and (\d+) obsidian.", s)
    return (int(match[1]), 0, int(match[2]), 0)


def parse_blueprints(data):
    for line in data.splitlines():
        ident = parse_blueprint_ident(line)
        blueprint = (
            parse_cost_ore_robot(line),
            parse_cost_clay_robot(line),
            parse_cost_obsidian_robot(line),
            parse_cost_geode_robot(line),
        )
        yield ident, blueprint


def heuristic(state):
    _, _, _, mined = state
    return 1000 * mined[3] + 100 * mined[2] + 10 * mined[1] + mined[0]


def search(costs, robots, duration, cache_size):
    best = 0
    seen = set()
    queue = [(0, robots, (0, 0, 0, 0), (0, 0, 0, 0))]
    depth = 0

    while queue:
        state = queue.pop(0)
        if state in seen:
            continue
        seen.add(state)

        t, robots, funds, mined = state

        if t == duration:
            best = max(best, mined[3])
            continue

        if t > depth:
            queue.sort(key=heuristic, reverse=True)
            queue = queue[:cache_size]
            depth = t

        # Consider not buying any robots.
        queue.append(
            (
                t + 1,
                robots,
                tuple(funds[i] + robots[i] for i in range(4)),
                tuple(mined[i] + robots[i] for i in range(4)),
            )
        )

        # Consider buying each robot that can be afforded.
        for robot in range(4):
            next_mined = tuple(mined[i] + robots[i] for i in range(4))
            if all(funds[i] >= costs[robot][i] for i in range(4)):
                next_funds = tuple(
                    funds[i] + robots[i] - costs[robot][i] for i in range(4)
                )
                next_robots = tuple(robots[i] + int(i == robot) for i in range(4))
                queue.append((t + 1, next_robots, next_funds, next_mined))

    return best


def run(data):
    blueprints = list(parse_blueprints(data))

    sum_quality_levels = 0
    for n, costs in blueprints:
        sum_quality_levels += n * search(
            costs, robots=(1, 0, 0, 0), duration=24, cache_size=256
        )

    product_max_geodes = 1
    for _, costs in blueprints[:3]:
        product_max_geodes *= search(
            costs, robots=(1, 0, 0, 0), duration=32, cache_size=8192
        )

    return sum_quality_levels, product_max_geodes
