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


def find_chain(unknown, start):
    parents = {}
    for k, (_, a, b) in unknown.items():
        parents[a] = k
        parents[b] = k

    chain = []
    child = start
    while child in parents:
        child = parents[child]
        chain.append(child)

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


def solve_chain_forwards(chain, known, pending, start):
    known = known.copy()

    known["humn"] = start
    for x in chain:
        op, a, b = pending[x]
        known[x] = calculate(op, known[a], known[b])

    return known["root"]


def solve_chain_backwards(chain, known, pending):
    known = known.copy()

    # Special case root, which now performs an equality check.
    _, a, b = pending.pop(chain[-1])
    if a in known:
        known[b] = known[a]
    else:
        known[a] = known[b]

    # Work backwards up the chain, inverting each operation to find the
    # input required to generate the known result.
    for x in reversed(chain[:-1]):
        op, a, b = pending[x]
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

    # Separate those monkeys whose unknown values depend on the value
    # yelled by "humn" from those which can be fixed irrespective of
    # that value.
    original = known.pop("humn")
    chain = find_chain(unknown, "humn")
    pending = {x: unknown.pop(x) for x in chain}

    # Resolve those monkeys whose value is unaffected by the value
    # yelled by "humn".
    resolve_fixed(known, unknown)

    part1 = solve_chain_forwards(chain, known, pending, original)
    part2 = solve_chain_backwards(chain, known, pending)

    return part1, part2
