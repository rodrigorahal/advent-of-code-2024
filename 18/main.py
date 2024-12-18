import fileinput
from collections import deque


def parse():
    coords = []
    for line in fileinput.input():
        col, row = line.strip().split(",")
        coords.append((int(row), int(col)))
    return coords


def simulate(coords):
    grid = {}
    for row, col in coords:
        grid[(row, col)] = "#"
    return grid


def search(grid, size=70):
    queue = deque([(0, 0, 0)])
    seen = set()
    while queue:
        row, col, steps = queue.popleft()

        if (row, col) in seen:
            continue
        seen.add((row, col))

        if (row, col) == (size, size):
            return steps

        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nrow, ncol = row + dr, col + dc
            if 0 <= nrow <= size and 0 <= ncol <= size and (nrow, ncol) not in grid:
                queue.append((nrow, ncol, steps + 1))
    return -1


def display(grid, size=70):
    for r in range(size + 1):
        row = []
        for c in range(size + 1):
            if (r, c) in grid:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))


def block(coords, size=70):
    for i in range(1024, len(coords)):
        grid = simulate(coords[: i + 1])
        steps = search(grid, size=size)
        if steps == -1:
            return coords[i]


def main():
    coords = parse()
    grid = simulate(coords[:1024])
    steps = search(grid, size=70)
    print(f"Part 1: {steps}")
    row, col = block(coords, size=70)
    print(f"Part 2: {col,row}")


if __name__ == "__main__":
    main()
