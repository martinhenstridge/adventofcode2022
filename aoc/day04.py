import re


def parse_pairs(data):
    for line in data.splitlines():
        match = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        yield int(match[1]), int(match[2]), int(match[3]), int(match[4])


def one_contains_other(a_lo, a_hi, b_lo, b_hi):
    return (a_lo <= b_lo and a_hi >= b_hi) or (b_lo <= a_lo and b_hi >= a_hi)


def one_overlaps_other(a_lo, a_hi, b_lo, b_hi):
    return a_hi >= b_lo if a_lo < b_lo else b_hi >= a_lo


def run(data):
    contains_count = 0
    overlaps_count = 0

    for a_lo, a_hi, b_lo, b_hi in parse_pairs(data):
        if one_contains_other(a_lo, a_hi, b_lo, b_hi):
            contains_count += 1
        if one_overlaps_other(a_lo, a_hi, b_lo, b_hi):
            overlaps_count += 1

    return contains_count, overlaps_count
