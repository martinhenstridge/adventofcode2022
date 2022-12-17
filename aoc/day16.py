import re


def parse_valves(data):
    valves = {}
    for line in data.splitlines():
        match = re.fullmatch(
            r"Valve ([A-Z]+) has flow rate=(\d+);"
            r" tunnel(?:s?) lead(?:s?) to valve(?:s?) (.+)",
            line,
        )
        valve = match[1]
        rate = int(match[2])
        options = match[3].split(", ")

        valves[valve] = rate, options
    return valves


def run(data):
    valves = parse_valves(data)
    edges = set()
    for k, v in valves.items():
        for o in v[1]:
            edges.add(tuple(sorted((k, o))))

    for e in edges:
        print(" -- ".join(e) + ";")

    print("AA [style=filled,color=red];")
    for k, v in valves.items():
        if v[0]:
            print(f"{k} [style=filled,color=blue];")
    return 0, 0
