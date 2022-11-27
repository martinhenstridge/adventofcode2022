from os.path import abspath, dirname, join


_ROOT = dirname(dirname(abspath(__file__)))


def get_input_lines(name):
    path = join(_ROOT, "inputs", name)
    with open(path) as f:
        return f.read().splitlines()
