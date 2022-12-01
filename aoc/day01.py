def parse_elf_totals(data):
    elf = 0
    for line in data.splitlines():
        if line:
            elf += int(line)
        else:
            yield elf
            elf = 0


def run(data):
    ordered = sorted(parse_elf_totals(data), reverse=True)

    top1 = ordered[0]
    top3 = sum(ordered[:3])

    return top1, top3
