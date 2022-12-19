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
    maxcost = tuple(max(cost) for cost in zip(*costs))
    best = 0
    depth = 0
    seen = set()

    state = (0, robots, (0, 0, 0, 0), (0, 0, 0, 0))
    queue = [state]

    while queue:
        t, robots, funds, mined = queue.pop(0)

        if t == duration:
            best = max(best, mined[3])
            continue

        if t > depth:
            queue.sort(key=heuristic, reverse=True)
            queue = queue[:cache_size]
            depth = t

        # Whatever we do on the current timestep, the same number of
        # minerals will always be mined.
        next_mined = tuple(mined[i] + robots[i] for i in range(4))
        next_funds = tuple(funds[i] + robots[i] for i in range(4))

        # Always buy a geode mining robot when possible.
        _robots = (robots[0], robots[1], robots[2], robots[3] + 1)
        _funds = tuple(next_funds[i] - costs[3][i] for i in range(4))
        if all(funds[i] >= costs[3][i] for i in range(4)):
            state = (t + 1, _robots, _funds, next_mined)
            if state not in seen:
                queue.append(state)
            continue

        # Consider buying each other type of robot that can be afforded.
        for r in range(3):
            # No point buying more robots to mine a particular mineral
            # if we're already mining enough to buy the most expensive
            # robot at every opportunity.
            if robots[r] >= maxcost[r]:
                continue

            # Can't afford the robot.
            if any(funds[i] < costs[r][i] for i in range(4)):
                continue

            _robots = tuple(robots[i] + int(i == r) for i in range(4))
            _funds = tuple(next_funds[i] - costs[r][i] for i in range(4))
            state = (t + 1, _robots, _funds, next_mined)
            if state not in seen:
                queue.append(state)

        # Finally, consider not buying any robots.
        state = (
            t + 1,
            robots,
            tuple(funds[i] + robots[i] for i in range(4)),
            next_mined,
        )
        if state not in seen:
            queue.append(state)

    return best


def run(data):
    blueprints = list(parse_blueprints(data))

    sum_quality_levels = 0
    for n, costs in blueprints:
        sum_quality_levels += n * search(
            costs, robots=(1, 0, 0, 0), duration=24, cache_size=100
        )

    product_max_geodes = 1
    for n, costs in blueprints[:3]:
        product_max_geodes *= search(
            costs, robots=(1, 0, 0, 0), duration=32, cache_size=6400
        )

    return sum_quality_levels, product_max_geodes
