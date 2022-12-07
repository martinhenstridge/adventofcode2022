import collections


def update_directory(old, new):
    if new == "/":
        return new
    if new == "..":
        return old.rpartition("/")[0]
    if old == "/":
        return old + new
    return old + "/" + new


def parse_list_entry(working, line):
    if line.startswith("dir "):
        return (True, update_directory(working, line[4:]))
    size, _ = line.split(maxsplit=1)
    return (False, int(size))


def parse_directories(data):
    directories = collections.defaultdict(list)
    working = None

    for line in data.splitlines():
        if line == "$ ls":
            continue
        elif line.startswith("$ cd "):
            working = update_directory(working, line[5:])
        else:
            entry = parse_list_entry(working, line)
            directories[working].append(entry)

    return directories


def calculate_size(directories, key):
    size = 0
    for entry in directories[key]:
        if entry[0]:
            size += calculate_size(directories, entry[1])
        else:
            size += entry[1]
    return size


def run(data):
    directories = parse_directories(data)
    sizes = {d: calculate_size(directories, d) for d in directories}

    total = 0
    for size in sizes.values():
        if size <= 100000:
            total += size

    excess = 30000000 - (70000000 - sizes["/"])
    smallest = sizes["/"]
    for directory, size in sizes.items():
        if size >= excess and size < smallest:
            smallest = size

    return total, smallest
