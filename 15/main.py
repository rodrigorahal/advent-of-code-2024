from collections import deque
import fileinput
from copy import deepcopy

DIRS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse():
    grid = []
    movements = []
    srow, scol = None, None
    S = ""
    for line in fileinput.input():
        S += line

    blocks = S.split("\n\n")

    for line in blocks[0].split("\n"):
        grid.append([char for char in line.strip()])

    for line in blocks[1].split("\n"):
        movements.extend([m for m in line.strip()])

    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "@":
                srow, scol = row, col
                break
    return grid, movements, srow, scol


def move(grid, srow, scol, movement):
    dr, dc = DIRS[movement]
    stack = []
    row, col = srow, scol

    while True:
        row += dr
        col += dc
        if grid[row][col] == "#":
            stack = []
            break
        if grid[row][col] == ".":
            stack.append((row - dr, col - dc))
            break
        if grid[row][col] == "O":
            stack.append((row - dr, col - dc))

    while stack:
        row, col = stack.pop()
        if (row, col) == (srow, scol):
            srow, scol = row + dr, col + dc
        grid[row + dr][col + dc] = grid[row][col]
        grid[row][col] = "."
    return grid, srow, scol


def move_large(grid, srow, scol, movement):
    dr, dc = DIRS[movement]
    queue = deque([(srow, scol)])
    stack = []
    seen = set()
    row, col = srow, scol
    while queue:
        row, col = queue.popleft()
        row += dr
        col += dc
        if (row, col) in seen:
            continue
        seen.add((row, col))
        if grid[row][col] == "#":
            stack = []
            break
        if grid[row][col] == ".":
            stack.append((row - dr, col - dc))
        if grid[row][col] == "[":
            queue.append((row, col))
            stack.append((row - dr, col - dc))
            if movement in ("^", "v"):
                queue.append((row, col + 1))
        if grid[row][col] == "]":
            queue.append((row, col))
            stack.append((row - dr, col - dc))
            if movement in ("^", "v"):
                queue.append((row, col - 1))

    while stack:
        row, col = stack.pop()
        if (row, col) == (srow, scol):
            srow, scol = row + dr, col + dc
        grid[row + dr][col + dc] = grid[row][col]
        grid[row][col] = "."
    return grid, srow, scol


def simulate(grid, movements, srow, scol, movef, v=False):
    grid = deepcopy(grid)

    for movement in movements:
        grid, srow, scol = movef(grid, srow, scol, movement)
        if v:
            print(f"Move: {movement}")
            display(grid)
    return grid


def gps(grid):
    c = 0
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "O" or char == "[":
                c += (100 * row) + col
    return c


def display(grid):
    for row in grid:
        print("".join(row))
    print()


def scaleup(grid):
    ggrid = []
    for row, cols in enumerate(grid):
        nrow = []
        for col, char in enumerate(cols):
            if char in ("#", "."):
                nrow.extend([char, char])
            elif char == "O":
                nrow.extend(["[", "]"])
            elif char == "@":
                nrow.extend(["@", "."])
        ggrid.append(nrow)
    srow, scol = None, None
    for row in range(len(ggrid)):
        for col in range(len(ggrid[0])):
            if ggrid[row][col] == "@":
                srow, scol = row, col
                break
    return ggrid, srow, scol


def main():
    grid, movements, srow, scol = parse()
    final = simulate(grid, movements, srow, scol, move)
    print(f"Part 1: {gps(final)}")

    scaled, srow, scol = scaleup(grid)
    final = simulate(scaled, movements, srow, scol, move_large)
    print(f"Part 2: {gps(final)}")


if __name__ == "__main__":
    main()
