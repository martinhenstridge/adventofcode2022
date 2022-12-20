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
    times = number.value % (len(numbers) - 1)

    if times == 0:
        return

    # Unlink number from its neighbours
    number._next._prev = number._prev
    number._prev._next = number._next

    # Find new home
    for _ in range(times):
        number._prev = number._next
        number._next = number._next._next

    # Link number to new neighbours
    number._next._prev = number
    number._prev._next = number


def mix(numbers, times):
    link(numbers)
    for _ in range(times):
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

    mix(numbers, 1)
    sum1 = sum(find(numbers, zero, idx).value for idx in (1000, 2000, 3000))

    for number in numbers:
        number.value *= 811589153
    mix(numbers, 10)
    sum2 = sum(find(numbers, zero, idx).value for idx in (1000, 2000, 3000))

    return sum1, sum2
