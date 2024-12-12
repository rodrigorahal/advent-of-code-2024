import fileinput
from collections import defaultdict, deque


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    return grid


def display(grid):
    for row in grid:
        print(row)


def plants(grid):
    s = set()
    for row in grid:
        for c in row:
            s.add(c)
    return s


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            ns.append((row + dr, col + dc))
    return ns


def search(grid, srow, scol, plant, seen):
    queue = deque([(srow, scol)])
    group = set()
    while queue:
        row, col = queue.popleft()

        if (row, col) in seen:
            continue
        seen.add((row, col))
        group.add((row, col, plant))

        for nr, nc in neighbors(grid, row, col):
            if grid[nr][nc] == plant:
                queue.append((nr, nc))
    return group


def groups(grid):
    seen = set()
    gs = []
    for row, cols in enumerate(grid):
        for col, plant in enumerate(cols):
            if (row, col) in seen:
                continue
            group = search(grid, row, col, plant, seen)
            gs.append(group)
    return gs


def perimeter(grid, group):
    H, W = len(grid), len(grid[0])
    p = 0
    for row, col, plant in group:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if not (
                0 <= row + dr < H
                and 0 <= col + dc < W
                and grid[row + dr][col + dc] == plant
            ):
                p += 1
    return p


def area(group):
    return len(group)


def price(grid, group):
    return area(group) * perimeter(grid, group)


def price_with_discount(grid, group):
    return area(group) * sides(grid, group)


def edges(grid, group):
    H, W = len(grid), len(grid[0])
    E = defaultdict(set)
    for row, col, plant in group:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if not (
                0 <= row + dr < H
                and 0 <= col + dc < W
                and grid[row + dr][col + dc] == plant
            ):
                E[(dr, dc)].add((row, col))
    return E


def sides(grid, group):
    s = 0
    for _, coords in edges(grid, group).items():
        seen = set()
        for row, col in coords:
            if (row, col) in seen:
                continue
            s += 1
            queue = deque([(row, col)])
            while queue:
                prow, pcol = queue.popleft()
                if (prow, pcol) in seen:
                    continue
                seen.add((prow, pcol))
                for nrow, ncol in neighbors(grid, prow, pcol):
                    if (nrow, ncol) in coords:
                        queue.append((nrow, ncol))
    return s


def main():
    grid = parse()
    print(f"Part 1: {sum(price(grid, group) for group in groups(grid))}")
    print(f"Part 2: {sum(price_with_discount(grid, group) for group in groups(grid))}")


if __name__ == "__main__":
    main()
