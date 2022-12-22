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
    maxlen = 1 + max(len(line) for line in lines)
    board.append(" " * maxlen)
    for line in data_board.splitlines():
        row = " " + line + " " * (maxlen - len(line))
        board.append(row)
    board.append(" " * maxlen)

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


def oob_wrap(board, row, col, facing):
    while board[row][col] == " ":
        row, col = next_tile(board, row, col, facing)
    return row, col, facing


def oob_cube(board, row, col, facing):
    pass


def move(board, row, col, facing, count, oob):
    r, c = row, col

    for _ in range(count):
        r, c = next_tile(board, row, col, facing)

        if board[r][c] == " ":
            r, c, facing = oob(board, r, c, facing)

        if board[r][c] == "#":
            break

        if board[r][c] == ".":
            row, col = r, c

    return row, col


def calculate_password(row, col, facing):
    return 1000 * row + 4 * col + facing


def follow_instructions(board, instructions, row, col, facing, oob):
    for instruction in instructions:
        if instruction == "L":
            facing = Facing((facing - 1) % 4)
        elif instruction == "R":
            facing = Facing((facing + 1) % 4)
        else:
            row, col = move(board, row, col, facing, instruction, oob)

    return calculate_password(row, col, facing)


def run(data):
    board, instructions = parse_board_instructions(data)

    row = 1
    col = board[row].find(".")
    facing = Facing.RIGHT

    password = follow_instructions(board, instructions, row, col, facing, oob_wrap)

    return password, 0
