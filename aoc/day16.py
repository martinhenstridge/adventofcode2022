import re
import math
import collections


def parse_valves(data):
    rates = {}
    links = collections.defaultdict(lambda: math.inf)

    for line in data.splitlines():
        match = re.fullmatch(
            r"Valve ([A-Z]+) has flow rate=(\d+);"
            r" tunnel(?:s?) lead(?:s?) to valve(?:s?) (.+)",
            line,
        )
        valve = match[1]
        rates[valve] = int(match[2])
        for other in match[3].split(", "):
            links[valve, other] = 1

    return rates, links


def search(rates, options, current_valve, open_valves, time_remaining):
    if time_remaining <= 0:
        return 0

    best = 0
    for v, t in options[current_valve].items():
        if v in open_valves:
            continue
        total = (time_remaining - t) * rates[v] + search(
            rates, options, v, open_valves | frozenset([v]), time_remaining - t
        )
        if total > best:
            best = total
    return best


def run(data):
    rates, links = parse_valves(data)

    # Use Floyd-Warshall algorithm to find shortest path from each valve
    # to every other valve.
    valves = tuple(rates)
    for k in valves:
        for i in valves:
            for j in valves:
                links[i, j] = min(links[i, j], links[i, k] + links[k, j])

    # Transform shortest path data into a more convenient format,
    # removing valves with zero flow rate and incrementing each
    # "distance" by 1 to account for the time taken to open the valve
    # after reaching it.
    options = collections.defaultdict(dict)
    for (a, b), d in links.items():
        if (
            a != b
            and rates[b] > 0
            and (a == "AA" or rates[a] > 0)
        ):
            options[a][b] = d + 1

    best1 = search(rates, options, "AA", frozenset(), 30)
    best2 = 0

    return best1, best2
