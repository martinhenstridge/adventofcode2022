SNAFU_DIGITS = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def from_snafu(snafu):
    n = 0
    factor = 1
    for char in reversed(snafu):
        n += SNAFU_DIGITS[char] * factor
        factor *= 5
    return n


def into_snafu(n):
    # Start with a 1 followed by only =s, i.e. the smallest value which
    # contains that number of digits. Keep adding =s until we're bigger
    # than the target value, then drop the last one to end up with the
    # correct number of digits.
    digits = ["1"]
    while from_snafu(digits) < n:
        digits.append("=")
    digits = digits[:-1]

    # For each digit in turn, moving from left to right, bump each digit
    # until we either hit a value that's bigger than the target or we
    # exhaust the potential values for that digit. Eventually we must
    # exactly match the target value, since we started with the smallest
    # possible value with the right number of digits.
    for i, digit in enumerate(digits):
        for alternative in ("-", "0", "1", "2"):
            snafu = digits[:i] + [alternative] + digits[i + 1 :]
            if from_snafu(snafu) > n:
                break
            digits = snafu

    return "".join(digits)


def run(data):
    total = sum(from_snafu(line) for line in data.splitlines())
    return (into_snafu(total),)
