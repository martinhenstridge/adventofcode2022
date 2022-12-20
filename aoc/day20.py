class Number:
    __slots__ = ("value", "_prev", "_next")

    def __init__(self, value):
        self.value = int(value)
        self._prev = None
        self._next = None


def link(numbers):
    for i, number in enumerate(numbers):
        if i == 0:
            number._prev = numbers[-1]
            number._next = numbers[1]
        elif i == len(numbers) - 1:
            number._prev = numbers[-2]
            number._next = numbers[0]
        else:
            number._prev = numbers[i - 1]
            number._next = numbers[i + 1]


def mix_number(numbers, number):
    # Avoid multiple laps around the ring. The -1 arises from the fact
    # that it only takes n-1 moves to return to the original ordering
    # for an n-element ring. For example, consider the value 'N' moving
    # around a ring containing 4 elements:
    #
    # start:   N x y z  ==  N x y z
    # step 1:  x N y z  ==  N y z x
    # step 2:  x y N z  ==  N z x y
    # step 3:  x y z N  ==  N x y z
    #
    # After 3 steps (= 4-1) the ordering is the same as it was at the
    # start, i.e. 'N' resides after 'z' and before 'x'.
    moves = number.value % (len(numbers) - 1)

    # Early exit if the destination is the same as the starting point.
    if moves == 0:
        return

    # Optimisation: if the destination is more than half way around the
    # ring moving clockwise, move anti-clockwise instead.
    reverse = moves > len(numbers) // 2
    if reverse:
        moves = len(numbers) - 1 - moves

    # Unlink number from its neighbours
    number._next._prev = number._prev
    number._prev._next = number._next

    # Find new home
    if reverse:
        for _ in range(moves):
            number._next = number._prev
            number._prev = number._prev._prev
    else:
        for _ in range(moves):
            number._prev = number._next
            number._next = number._next._next

    # Link number to new neighbours
    number._next._prev = number
    number._prev._next = number


def mix(numbers, rounds, multiplier):
    link(numbers)
    for number in numbers:
        number.value *= multiplier

    for _ in range(rounds):
        for number in numbers:
            mix_number(numbers, number)


def find(numbers, start, index):
    number = start
    for _ in range(index % len(numbers)):
        number = number._next
    return number


def run(data):
    numbers = [Number(line) for line in data.splitlines()]
    zero = next(n for n in numbers if n.value == 0)

    mix(numbers, 1, 1)
    sum1 = sum(find(numbers, zero, idx).value for idx in (1000, 2000, 3000))

    mix(numbers, 10, 811589153)
    sum2 = sum(find(numbers, zero, idx).value for idx in (1000, 2000, 3000))

    return sum1, sum2
