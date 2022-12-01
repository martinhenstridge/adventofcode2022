def parse_elf_totals(data):
    elves = []

    elf = 0
    for line in data.splitlines():
        if line:
            elf += int(line)
        else:
            elves.append(elf)
            elf = 0

    return elves


def run(data):
    totals = parse_elf_totals(data)
    ordered = sorted(totals, reverse=True)

    top1 = ordered[0]
    top3 = sum(ordered[:3])

    return top1, top3
