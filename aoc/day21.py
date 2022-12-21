def parse_monkeys(data):
    known = {}
    unknown = {}
    for line in data.splitlines():
        name, job = line.split(": ", maxsplit=1)
        if " " not in job:
            known[name] = int(job)
        else:
            a, op, b = job.split(" ", maxsplit=2)
            unknown[name] = op, a, b
    return known, unknown


def calculate(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a // b
    assert False


def find_dependency_chain(unknown, start):
    parents = {}
    for k, (_, a, b) in unknown.items():
        parents[a] = k
        parents[b] = k

    chain = {}
    child = start
    while child in parents:
        child = parents[child]
        chain[child] = unknown.pop(child)

    return chain


def resolve_fixed(known, unknown):
    while unknown:
        still_unknown = {}
        for name, (op, a, b) in unknown.items():
            try:
                known[name] = calculate(op, known[a], known[b])
            except KeyError:
                still_unknown[name] = (op, a, b)
        unknown = still_unknown


def solve_chain_forwards(chain, known, start):
    known["humn"] = start
    for x, (op, a, b) in chain.items():
        known[x] = calculate(op, known[a], known[b])

    return known["root"]


def solve_chain_backwards(chain, known):
    # Special case root, which now performs an equality check.
    _, a, b = chain.pop("root")
    if a in known:
        known[b] = known[a]
    else:
        known[a] = known[b]

    # Work backwards up the chain, inverting each operation to find the
    # input required to generate the known result.
    for x, (op, a, b) in reversed(chain.items()):
        if op == "+":
            if a in known:
                known[b] = known[x] - known[a]
            else:
                known[a] = known[x] - known[b]
        elif op == "-":
            if a in known:
                known[b] = known[a] - known[x]
            else:
                known[a] = known[x] + known[b]
        elif op == "*":
            if a in known:
                known[b] = known[x] // known[a]
            else:
                known[a] = known[x] // known[b]
        elif op == "/":
            if a in known:
                known[b] = known[a] / known[x]
            else:
                known[a] = known[x] * known[b]

    return known["humn"]


def run(data):
    known, unknown = parse_monkeys(data)
    original = known.pop("humn")

    # Separate those monkeys whose unknown values depend on the value
    # yelled by "humn" from those which can be fixed irrespective of
    # that value.
    chain = find_dependency_chain(unknown, "humn")

    # Resolve those monkeys whose values are unaffected by the value
    # yelled by "humn".
    resolve_fixed(known, unknown)

    part1 = solve_chain_forwards(chain, known.copy(), original)
    part2 = solve_chain_backwards(chain, known.copy())

    return part1, part2
