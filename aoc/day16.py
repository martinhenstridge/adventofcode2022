import re
import math
import collections


def parse_valves(data):
    rates = {}
    links = collections.defaultdict(lambda: math.inf)

    for line in data.splitlines():
        match = re.fullmatch(
            r"Valve ([A-Z]+) has flow rate=(\d+);" r" tunnels? leads? to valves? (.+)",
            line,
        )
        valve = match[1]
        rates[valve] = int(match[2])
        for other in match[3].split(", "):
            links[valve, other] = 1

    return rates, links


def search(rates, options, current_valve, open_valves, time_remaining, flow, results):
    if flow > results[open_valves]:
        results[open_valves] = flow

    for v, t in options[current_valve].items():
        new_time_remaining = time_remaining - t
        if v in open_valves:
            continue
        if new_time_remaining <= 0:
            continue
        search(
            rates,
            options,
            v,
            open_valves | frozenset([v]),
            new_time_remaining,
            flow + new_time_remaining * rates[v],
            results,
        )
    return results


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
        if a != b and rates[b] > 0 and (a == "AA" or rates[a] > 0):
            options[a][b] = d + 1

    results1 = search(
        rates, options, "AA", frozenset(), 30, 0, collections.defaultdict(int)
    )
    results2 = search(
        rates, options, "AA", frozenset(), 26, 0, collections.defaultdict(int)
    )
    best1 = max(results1.values())
    best2 = max(
        v1 + v2
        for k1, v1 in results2.items()
        for k2, v2 in results2.items()
        if not k1 & k2
    )

    return best1, best2
