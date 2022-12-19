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


def run(data):
    rates, links = parse_valves(data)

    valves = tuple(rates)
    for k in valves:
        for i in valves:
            for j in valves:
                links[i, j] = min(links[i, j], links[i, k] + links[k, j])

    ds = {}
    for (a, b), d in links.items():
        if (a == "AA" or rates[a] > 0) and (b == "AA" or rates[b] > 0):
            ds[a, b] = d

    for k, v in ds.items():
        print(k, v)

    print(len(links), len(ds))

    return 0, 0
