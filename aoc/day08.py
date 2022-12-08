def parse_grid(data):
    rows = 0
    cols = 0
    grid = []

    for line in data.splitlines():
        rows += 1
        cols = len(line)
        grid.append([int(char) for char in line])

    return grid, rows, cols


def mark_visible_along_row(visible, grid, row, col_range):
    tallest = -1
    for col in col_range:
        tree = grid[row][col]
        if tree > tallest:
            tallest = tree
            visible[row][col] = True


def mark_visible_along_col(visible, grid, col, row_range):
    tallest = -1
    for row in row_range:
        tree = grid[row][col]
        if tree > tallest:
            tallest = tree
            visible[row][col] = True


def find_visible(grid, rows, cols):
    visible = [[False for col in range(cols)] for row in range(rows)]

    for row in range(rows):
        mark_visible_along_row(visible, grid, row, range(cols))
        mark_visible_along_row(visible, grid, row, range(cols - 1, -1, -1))

    for col in range(cols):
        mark_visible_along_col(visible, grid, col, range(rows))
        mark_visible_along_col(visible, grid, col, range(rows - 1, -1, -1))

    return visible


def viewing_distance_along_row(grid, height, col, row_range):
    count = 0
    for row in row_range:
        count += 1
        if grid[row][col] >= height:
            break
    return count


def viewing_distance_along_col(grid, height, row, col_range):
    count = 0
    for col in col_range:
        count += 1
        if grid[row][col] >= height:
            break
    return count


def scenic_score(grid, rows, cols, row, col):
    height = grid[row][col]

    score = 1
    score *= viewing_distance_along_row(grid, height, col, range(row + 1, rows))
    score *= viewing_distance_along_row(grid, height, col, range(row -1, -1, -1))
    score *= viewing_distance_along_col(grid, height, row, range(col + 1, cols))
    score *= viewing_distance_along_col(grid, height, row, range(col -1, -1, -1))

    return score


def run(data):
    grid, rows, cols = parse_grid(data)
    visible = find_visible(grid, rows, cols)

    visible_count = sum(int(tree) for row in visible for tree in row)
    max_scenic_score = max(
        scenic_score(grid, rows, cols, row, col)
        for row in range(rows) for col in range(cols)
    )

    return visible_count, max_scenic_score
