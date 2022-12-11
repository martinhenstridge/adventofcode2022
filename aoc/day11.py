import re
import copy
import typing
import operator
import dataclasses


@dataclasses.dataclass
class Monkey:
    count: int
    items: typing.List[int]
    operation: typing.Callable
    operand: typing.Optional[int]
    divisor: int
    where_true: int
    where_false: int


MONKEY_REGEX = r"""Monkey (\d+):
  Starting items: (.+)
  Operation: new = old ([\+\*]) (\d+|old)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)
"""


def parse_monkey(match):
    which = int(match[1])
    monkey = Monkey(
        count=0,
        items=[int(n) for n in match[2].split(", ")],
        operation=operator.add if match[3] == "+" else operator.mul,
        operand=None if match[4] == "old" else int(match[4]),
        divisor=int(match[5]),
        where_true=int(match[6]),
        where_false=int(match[7]),
    )
    return which, monkey


def parse_monkeys(data):
    monkeys = []
    for match in re.finditer(MONKEY_REGEX, data, re.MULTILINE):
        which, monkey = parse_monkey(match)
        monkeys.insert(which, monkey)
    return monkeys


def run_round(monkeys, decrease):
    for monkey in monkeys:
        for worry_level in monkey.items:
            operand = monkey.operand or worry_level
            worry_level = decrease(monkey.operation(worry_level, operand))
            where = (
                monkey.where_true
                if worry_level % monkey.divisor == 0
                else monkey.where_false
            )
            monkeys[where].items.append(worry_level)
        monkey.count += len(monkey.items)
        monkey.items = []


def run_keep_away(starting, rounds, decrease):
    monkeys = copy.deepcopy(starting)

    for _ in range(rounds):
        run_round(monkeys, decrease)

    ordered = sorted(monkeys, key=lambda m: m.count, reverse=True)
    return ordered[0].count * ordered[1].count


def run(data):
    starting = parse_monkeys(data)

    modulus = 1
    for monkey in starting:
        modulus *= monkey.divisor

    return (
        run_keep_away(starting, 20, lambda worry: worry // 3),
        run_keep_away(starting, 10000, lambda worry: worry % modulus),
    )
