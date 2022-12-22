import enum


class Facing(enum.IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def parse_board_instructions(data):
    data_board, data_instructions = data.split("\n\n", maxsplit=1)

    board = []
    lines = data_board.splitlines()
    maxlen = max(len(line) for line in lines)
    for line in data_board.splitlines():
        row = line + " " * (maxlen - len(line))
        board.append(row)

    instructions = []
    for i in data_instructions.replace("L", ",L,").replace("R", ",R,").split(","):
        if i == "L" or i == "R":
            instructions.append(i)
        else:
            instructions.append(int(i))

    return board, instructions


def next_tile(board, row, col, facing):
    if facing is Facing.RIGHT:
        col += 1
        if col >= len(board[row]):
            col = 0
    elif facing is Facing.DOWN:
        row += 1
        if row >= len(board):
            row = 0
    elif facing is Facing.LEFT:
        col -= 1
        if col < 0:
            col = len(board[row]) - 1
    elif facing is Facing.UP:
        row -= 1
        if row < 0:
            row = len(board) - 1

    return row, col


def move(board, row, col, facing, count):
    r, c = row, col

    for _ in range(count):
        r, c = next_tile(board, row, col, facing)
        tile = board[r][c]

        while tile == " ":
            r, c = next_tile(board, r, c, facing)
            tile = board[r][c]

        if tile == "#":
            break

        if tile == ".":
            row, col = r, c

    return row, col


def calculate_password(row, col, facing):
    return 1000 * (row + 1) + 4 * (col + 1) + facing


def follow_instructions(board, instructions, row, col, facing):
    for instruction in instructions:
        if instruction == "L":
            facing = Facing((facing - 1) % 4)
        elif instruction == "R":
            facing = Facing((facing + 1) % 4)
        else:
            row, col = move(board, row, col, facing, instruction)

    return calculate_password(row, col, facing)


def run(data):
    board, instructions = parse_board_instructions(data)

    row = 0
    col = board[0].find(".")
    facing = Facing.RIGHT

    password = follow_instructions(board, instructions, row, col, facing)

    return password, 0
