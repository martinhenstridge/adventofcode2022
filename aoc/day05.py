import re
import collections


def split_input_data(data):
    lines = data.splitlines()
    for idx, line in enumerate(lines):
        if not line:
            return lines[:idx], lines[idx + 1 :]


def parse_stacks(lines):
    head = lines[-1]
    tail = lines[-2::-1]

    stacks = collections.defaultdict(list)
    for i in range(1, len(head), 4):
        stack = head[i]
        for line in tail:
            if line[i] == " ":
                break
            stacks[stack].append(line[i])
    return stacks


def parse_moves(lines):
    moves = []
    for line in lines:
        match = re.match(r"move (\d+) from (\d+) to (\d+)", line)
        move = int(match[1]), match[2], match[3]
        moves.append(move)
    return moves


def rearrange_singly(stacks, count, src, dst):
    for _ in range(count):
        moving = stacks[src].pop()
        stacks[dst].append(moving)


def rearrange_multiply(stacks, count, src, dst):
    moving = stacks[src][-count:]
    stacks[dst].extend(moving)
    stacks[src] = stacks[src][:-count]


def rearrange(starting, moves, func):
    stacks = {stack: crates.copy() for stack, crates in starting.items()}
    for count, src, dst in moves:
        func(stacks, count, src, dst)
    return "".join(stack[-1] for stack in stacks.values())


def run(data):
    stack_lines, move_lines = split_input_data(data)
    stacks = parse_stacks(stack_lines)
    moves = parse_moves(move_lines)

    tops1 = rearrange(stacks, moves, rearrange_singly)
    tops2 = rearrange(stacks, moves, rearrange_multiply)

    return tops1, tops2
