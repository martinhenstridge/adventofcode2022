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
    board.append(" " * (2 + maxlen))
    for line in data_board.splitlines():
        row = " " + line + " " * (maxlen - len(line)) + " "
        board.append(row)
    board.append(" " * (2 + maxlen))

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
        if col == len(board[row]):
            col = 0
    elif facing is Facing.DOWN:
        row += 1
        if row == len(board):
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
    # The input shape is as follows:
    #
    #           __a__ __b__
    #          |     |     |
    #          n     |     c
    #          |_____|__d__|
    #          |     |
    #          m     e
    #     __l__|_____|
    #    |     |     |
    #    k     |     f
    #    |_____|__g__|
    #    |     |
    #    j     h
    #    |__i__|
    #
    if facing is Facing.RIGHT:
        # c -> f
        if 1 <= row <= 50:
            return 151 - row, 100, Facing.LEFT

        # e -> d
        if 51 <= row <= 100:
            return 50, row + 50, Facing.UP

        # f -> c
        if 101 <= row <= 150:
            return 151 - row, 150, Facing.LEFT

        # h -> g
        if 151 <= row <= 200:
            return 150, row - 100, Facing.UP

    if facing is Facing.DOWN:
        # i -> b
        if 1 <= col <= 50:
            return 1, col + 100, Facing.DOWN

        # g -> h
        if 51 <= col <= 100:
            return col + 100, 50, Facing.LEFT

        # d -> e
        if 101 <= col <= 150:
            return col - 50, 100, Facing.LEFT

    if facing is Facing.LEFT:
        # n -> k
        if 1 <= row <= 50:
            return 151 - row, 1, Facing.RIGHT

        # m -> l
        if 51 <= row <= 100:
            return 101, row - 50, Facing.DOWN

        # k -> n
        if 101 <= row <= 150:
            return 151 - row, 51, Facing.RIGHT

        # j -> a
        if 151 <= row <= 200:
            return 1, row - 100, Facing.DOWN

    if facing is Facing.UP:
        # l -> m
        if 1 <= col <= 50:
            return col + 50, 51, Facing.RIGHT

        # a -> j
        if 51 <= col <= 100:
            return col + 100, 1, Facing.RIGHT

        # b -> i
        if 101 <= col <= 150:
            return 200, col - 100, Facing.UP

    assert False


def move(board, row, col, facing, count, oob):
    for _ in range(count):
        f = facing
        r, c = next_tile(board, row, col, facing)

        if board[r][c] == " ":
            r, c, f = oob(board, r, c, f)

        if board[r][c] == "#":
            break

        if board[r][c] == ".":
            row, col, facing = r, c, f

    return row, col, facing


def follow_instructions(board, instructions, oob):
    row = 1
    col = board[row].find(".")
    facing = Facing.RIGHT

    for instruction in instructions:
        if instruction == "L":
            facing = Facing((facing - 1) % 4)
        elif instruction == "R":
            facing = Facing((facing + 1) % 4)
        else:
            row, col, facing = move(board, row, col, facing, instruction, oob)

    return 1000 * row + 4 * col + facing


def run(data):
    board, instructions = parse_board_instructions(data)

    password1 = follow_instructions(board, instructions, oob_wrap)
    password2 = follow_instructions(board, instructions, oob_cube)

    return password1, password2
