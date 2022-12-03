def get_priority(item):
    if item.islower():
        return ord(item) - 96
    if item.isupper():
        return ord(item) - 38
    assert False


def find_common_among_halves(rucksacks):
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        common = set(rucksack[:half]) & set(rucksack[half:])
        yield get_priority(common.pop())


def find_common_among_threes(rucksacks):
    for i in range(len(rucksacks) // 3):
        common = (
            set(rucksacks[0 + i * 3]) &
            set(rucksacks[1 + i * 3]) &
            set(rucksacks[2 + i * 3])
        )
        yield get_priority(common.pop())


def run(data):
    rucksacks = data.splitlines()

    total1 = sum(p for p in find_common_among_halves(rucksacks))
    total2 = sum(p for p in find_common_among_threes(rucksacks))

    return total1, total2
