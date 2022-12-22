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
    if facing is Facing.RIGHT:
        # 3 -> 6
        if 1 <= row <= 50:
            print("3 -> 6")
            assert col == 151
            return 151 - row, 100, Facing.LEFT

        # 5 -> 4
        if 51 <= row <= 100:
            print("5 -> 4")
            assert col == 101
            return 50, row + 50, Facing.UP

        # 6 -> 3
        if 101 <= row <= 150:
            print("6 -> 3")
            assert col == 101
            return 151 - row, 150, Facing.LEFT

        # 8 -> 7
        if 151 <= row <= 200:
            print("8 -> 7")
            assert col == 51
            return 150, row - 100, Facing.UP

    if facing is Facing.DOWN:
        # 9 -> 2
        if 1 <= col <= 50:
            print("9 -> 2")
            assert row == 201
            return 1, col + 100, Facing.DOWN

        # 7 -> 8
        if 51 <= col <= 100:
            print("7 -> 8")
            assert row == 151
            return col + 100, 50, Facing.LEFT

        # 4 -> 5
        if 101 <= col <= 150:
            print("4 -> 5")
            assert row == 51
            return col - 50, 100, Facing.LEFT

    if facing is Facing.LEFT:
        # 14 -> 11
        if 1 <= row <= 50:
            print("14 -> 11")
            assert col == 50
            return 151 - row, 1, Facing.LEFT

        # 13 -> 12
        if 51 <= row <= 100:
            print("13 -> 12")
            assert col == 50
            return 101, row - 50, Facing.DOWN

        # 11 -> 14
        if 101 <= row <= 150:
            print("11 -> 14")
            assert col == 0
            return 151 - row, 51, Facing.RIGHT

        # 10 -> 1
        if 151 <= row <= 200:
            print("10 -> 1")
            assert col == 0
            return 1, row - 100, Facing.DOWN

    if facing is Facing.UP:
        # 12 -> 13
        if 1 <= col <= 50:
            print("12 -> 13")
            assert row == 100
            return col + 50, 51, Facing.RIGHT

        # 1 -> 10
        if 51 <= col <= 100:
            print("1 -> 10")
            assert row == 0
            return col + 100, 1, Facing.RIGHT

        # 2 -> 9
        if 101 <= col <= 150:
            print("2 -> 9")
            assert row == 0
            return 200, col - 100, Facing.UP

    assert False


def move(board, row, col, facing, count, oob):
    for _ in range(count):
        f = facing
        r, c = next_tile(board, row, col, facing)

        if board[r][c] == " ":
            print("heading oob:", r, c, f)
            r, c, f = oob(board, r, c, f)
            print("arrived at:", r, c, f)
            assert 0 <= r < len(board)
            assert 0 <= c < len(board[0])
            assert board[r][c] != " "

        if board[r][c] == "#":
            pass
            #break

        if board[r][c] == ".":
            row, col, facing = r, c, f

    return row, col, facing


def calculate_password(row, col, facing):
    return 1000 * row + 4 * col + facing


def follow_instructions(board, instructions, oob):
    row = 1
    col = board[row].find(".")
    facing = Facing.RIGHT
    print("start", row, col, facing)

    for instruction in instructions:
        if instruction == "L":
            facing = Facing((facing - 1) % 4)
        elif instruction == "R":
            facing = Facing((facing + 1) % 4)
        else:
            row, col, facing = move(board, row, col, facing, instruction, oob)
        print("instruction", instruction, row, col, facing)

    print("finish", row, col, facing)
    return calculate_password(row, col, facing)


def run(data):
    board, instructions = parse_board_instructions(data)

    follow_instructions(board, ["R", 200], oob_cube)
    #follow_instructions(board, ["R", "R", "R", 200], oob_cube)

    #password1 = follow_instructions(board, instructions, oob_wrap)
    #password2 = follow_instructions(board, instructions, oob_cube)
    password1 = 0
    password2 = 0

    return password1, password2

"""
# 1 -> 10
assert oob_cube(None, 0, 51, Facing.UP) == (151, 1, Facing.RIGHT)
assert oob_cube(None, 0, 100, Facing.UP) == (200, 1, Facing.RIGHT)

# 2 -> 9
assert oob_cube(None, 0, 101, Facing.UP) == (200, 1, Facing.UP)
assert oob_cube(None, 0, 150, Facing.UP) == (200, 50, Facing.UP)

# 3 -> 6
assert oob_cube(None, 1, 151, Facing.RIGHT) == (150, 100, Facing.LEFT)
assert oob_cube(None, 50, 151, Facing.RIGHT) == (101, 100, Facing.LEFT)

# 4 -> 5
assert oob_cube(None, 51, 101, Facing.DOWN) == (51, 100, Facing.LEFT)
assert oob_cube(None, 51, 150, Facing.DOWN) == (100, 100, Facing.LEFT)

# 5 -> 4
assert oob_cube(None, 51, 101, Facing.RIGHT) == (50, 101, Facing.UP)
assert oob_cube(None, 100, 101, Facing.RIGHT) == (50, 150, Facing.UP)

# 6 -> 3
assert oob_cube(None, 51, 101, Facing.RIGHT) == (50, 101, Facing.UP)
assert oob_cube(None, 100, 101, Facing.RIGHT) == (50, 150, Facing.UP)

# 7 -> 8
assert oob_cube(None, 151, 51, Facing.DOWN) == (151, 50, Facing.LEFT)
assert oob_cube(None, 151, 100, Facing.DOWN) == (200, 50, Facing.LEFT)

# 8 -> 7
assert oob_cube(None, 151, 51, Facing.RIGHT) == (150, 51, Facing.UP)
assert oob_cube(None, 200, 51, Facing.RIGHT) == (150, 100, Facing.UP)

# 9 -> 2
assert oob_cube(None, 201, 1, Facing.DOWN) == (1, 101, Facing.DOWN)
assert oob_cube(None, 201, 50, Facing.DOWN) == (1, 150, Facing.DOWN)

# 10 -> 1
assert oob_cube(None, 151, 0, Facing.LEFT) == (1, 51, Facing.DOWN)
assert oob_cube(None, 200, 0, Facing.LEFT) == (1, 100, Facing.DOWN)

# 11 -> 14
assert oob_cube(None, , , Facing.) == (, , Facing.)
assert oob_cube(None, , , Facing.) == (, , Facing.)

# 12 -> 13
assert oob_cube(None, , , Facing.) == (, , Facing.)
assert oob_cube(None, , , Facing.) == (, , Facing.)

# 13 -> 12
assert oob_cube(None, , , Facing.) == (, , Facing.)
assert oob_cube(None, , , Facing.) == (, , Facing.)

# 14 -> 11
assert oob_cube(None, , , Facing.) == (, , Facing.)
assert oob_cube(None, , , Facing.) == (, , Facing.)
"""
