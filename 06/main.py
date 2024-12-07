import fileinput
from copy import deepcopy


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    r, c = None, None
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "^":
                r, c = row, col
                break
    return grid, r, c


def display(grid):
    for row in grid:
        print(row)


def turn(dr, dc):
    if (dr, dc) == (-1, 0):
        return (0, 1)
    if (dr, dc) == (0, 1):
        return (1, 0)
    if (dr, dc) == (1, 0):
        return (0, -1)
    if (dr, dc) == (0, -1):
        return (-1, 0)


def walk(grid, srow, scol, dr, dc):
    H, W = len(grid), len(grid[0])
    row, col = srow, scol
    seen = set()
    seen_with_dir = set()
    while True:
        if not (0 <= row < H and 0 <= col < W):
            break
        seen.add((row, col))
        if not (0 <= row + dr < H and 0 <= col + dc < W):
            break
        if (row, col, dr, dc) in seen_with_dir:
            return -1
        seen_with_dir.add((row, col, dr, dc))
        if grid[row + dr][col + dc] == "#":
            dr, dc = turn(dr, dc)
        else:
            row, col = row + dr, col + dc

    return len(seen)


def loops(grid, srow, scol, dr, dc):
    H, W = len(grid), len(grid[0])
    count = 0
    for row in range(H):
        for col in range(W):
            if grid[row][col] == "#" or (row, col) == (srow, scol):
                continue
            ngrid = deepcopy(grid)
            ngrid[row] = ngrid[row][:col] + "#" + ngrid[row][col + 1 :]
            if walk(ngrid, srow, scol, dr, dc) == -1:
                count += 1
    return count


def main():
    grid, row, col = parse()
    print(f"Part 1: {walk(grid, row, col, -1, 0)}")
    print(f"Part 2: {loops(grid, row, col, -1, 0)}")


if __name__ == "__main__":
    main()
