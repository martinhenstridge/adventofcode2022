import sys
import time
import pathlib

from . import DAYS

_INPUTS = pathlib.Path(__file__).parents[1] / "inputs"


def run(day, solver, solutions):
    start = time.perf_counter()
    with open(_INPUTS / day) as f:
        data = f.read()
    results = solver.run(data)
    end = time.perf_counter()

    print()
    for idx, result in enumerate(results):
        print(f"[{day}/{idx+1}] {result}")
    print(f"{1000 * (end - start):.3f}ms")
    assert results == solutions


if len(sys.argv) > 1:
    day = sys.argv[1]
    run(day, *DAYS[day])
else:
    for day in DAYS:
        run(day, *DAYS[day])
