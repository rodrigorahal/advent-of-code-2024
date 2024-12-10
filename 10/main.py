import fileinput
from collections import deque


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    return grid


def display(grid):
    for row in grid:
        print(row)


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            ns.append((row + dr, col + dc))
    return ns


def search(grid, srow, scol, with_path=False):
    if with_path:
        queue = deque([(srow, scol, ((srow, scol)))])
    else:
        queue = deque([(srow, scol)])
    seen = set()
    score = 0

    while queue:
        if with_path:
            row, col, path = queue.popleft()
            if (row, col, path) in seen:
                continue
            seen.add((row, col, path))
        else:
            row, col = queue.popleft()
            if (row, col) in seen:
                continue
            seen.add((row, col))

        if grid[row][col] == "9":
            score += 1
            continue

        for nrow, ncol in neighbors(grid, row, col):
            if (nrow, ncol) in seen or grid[nrow][ncol] == ".":
                continue
            h = int(grid[row][col])
            nh = int(grid[nrow][ncol])
            if nh == h + 1:
                if with_path:
                    queue.append((nrow, ncol, path + (nrow, ncol)))
                else:
                    queue.append((nrow, ncol))
    return score


def hike(grid, with_path=False):
    scores = 0
    for row, cols in enumerate(grid):
        for col, height in enumerate(cols):
            if height == "0":
                scores += search(grid, row, col, with_path)
    return scores


def main():
    grid = parse()
    print(f"Part 1: {hike(grid)}")
    print(f"Part 2: {hike(grid, with_path=True)}")


if __name__ == "__main__":
    main()
