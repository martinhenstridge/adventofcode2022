import enum


class Instruction(enum.Enum):
    NOOP = 0
    ADDX = 1


def parse_instructions(data):
    for line in data.splitlines():
        if line == "noop":
            yield Instruction.NOOP, 0
        elif line.startswith("addx"):
            yield Instruction.ADDX, int(line[5:])


def run_cpu(instructions):
    x = 1
    cycle = 1

    for instruction, value in instructions:
        if instruction is Instruction.NOOP:
            yield cycle, x
            cycle += 1
        elif instruction is Instruction.ADDX:
            yield cycle, x
            cycle += 1
            yield cycle, x
            cycle += 1
            x += value


def signal_strengths(instructions):
    for cycle, x in run_cpu(instructions):
        if cycle in (20, 60, 100, 140, 180, 220):
            yield cycle * x


def draw_crt(instructions):
    drawing = 0
    print()

    for cycle, x in run_cpu(instructions):
        if (drawing == x - 1) or (drawing == x) or (drawing == x + 1):
            print(" #", end="")
        else:
            print(" .", end="")

        drawing += 1
        if drawing == 40:
            drawing = 0
            print()


def run(data):
    instructions = [i for i in parse_instructions(data)]

    sum_signal_strengths = sum(ss for ss in signal_strengths(instructions))
    draw_crt(instructions)

    return sum_signal_strengths, "RZHFGJCB"
