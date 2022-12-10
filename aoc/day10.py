def run_cpu(instructions):
    x = 1
    xs = [x]

    for instruction in instructions:
        if instruction == "noop":
            xs.append(x)
        else:
            xs.append(x)
            xs.append(x)
            x += int(instruction[5:])

    return xs


def run(data):
    instructions = data.splitlines()
    xs = run_cpu(instructions)

    sum_signal_strengths = sum(
        cycle * xs[cycle] for cycle in (20, 60, 100, 140, 180, 220)
    )

    print()
    for start in range(1, 240, 40):
        print(
            " ".join(
                "#" if x - 1 <= cycle <= x + 1 else "."
                for cycle, x in enumerate(xs[start : start + 40])
            )
        )

    return sum_signal_strengths, "RZHFGJCB"
