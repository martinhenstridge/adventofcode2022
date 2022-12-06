def find_non_repeating(signal, count):
    for i in range(len(signal)):
        if len(set(signal[i : i + count])) == count:
            return i + count


def run(data):
    signal = data.strip()

    position1 = find_non_repeating(signal, 4)
    position2 = find_non_repeating(signal, 14)

    return position1, position2
