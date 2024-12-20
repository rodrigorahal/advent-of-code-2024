import fileinput
from collections import deque, Counter
from itertools import combinations


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    S, E = None, None
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "S":
                S = (row, col)
            if char == "E":
                E = (row, col)

    return grid, S, E


def search(grid, srow, scol, erow, ecol, cheat_at=None, go_to=None):
    H, W = len(grid), len(grid[0])
    queue = deque([(srow, scol, 0)])
    seen = set()
    while queue:
        row, col, steps = queue.popleft()
        if (row, col) == (erow, ecol):
            return steps

        if (row, col) in seen:
            continue
        seen.add((row, col))

        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nrow, ncol = row + dr, col + dc
            if 0 <= nrow < H and 0 <= ncol < W and grid[nrow][ncol] != "#":
                queue.append((nrow, ncol, steps + 1))

            if (
                cheat_at
                and (nrow, ncol) == cheat_at
                and 0 <= nrow < H
                and 0 <= ncol < W
                and grid[nrow][ncol] == "#"
            ):
                grow, gcol = go_to
                queue.append((grow, gcol, steps + 2))
    return -1


def cheat(grid, srow, scol, erow, ecol, curr):
    H, W = len(grid), len(grid[0])
    print(H, W)
    c = Counter()
    C = 0
    for row in range(1, H - 1):
        for col in range(1, W - 1):
            char = grid[row][col]
            if char == "#":
                for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nrow, ncol = row + dr, col + dc

                    if (
                        0 <= nrow < H
                        and 0 <= ncol < W
                        and grid[nrow][ncol] in (".", "E")
                    ):

                        steps = search(
                            grid, srow, scol, erow, ecol, (row, col), (nrow, ncol)
                        )
                        if steps > 0:
                            # print(f"{curr=} {steps=} {curr-steps=}")
                            c[curr - steps] += 1
                            if curr - steps >= 100:
                                C += 1
    return C


def display(grid):
    for row in grid:
        print(row)


def smart_cheat(grid, srow, scol, time_to_cheat=2):
    H, W = len(grid), len(grid[0])
    C = 0
    steps_to = {}
    queue = deque([(srow, scol, 0)])
    while queue:
        row, col, steps = queue.popleft()
        if (row, col) in steps_to:
            continue
        steps_to[(row, col)] = steps
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nrow, ncol = row + dr, col + dc
            if 0 <= nrow < H and 0 <= ncol < W and grid[nrow][ncol] != "#":
                queue.append((nrow, ncol, steps + 1))

    for ((arow, acol), steps_to_a), ((brow, bcol), steps_to_b) in combinations(
        steps_to.items(), 2
    ):
        steps_from_a_to_b_with_cheat = abs(brow - arow) + abs(bcol - acol)

        steps_from_a_to_b_wo_cheat = steps_to_b - steps_to_a

        can_save = steps_from_a_to_b_wo_cheat - steps_from_a_to_b_with_cheat

        if steps_from_a_to_b_with_cheat <= time_to_cheat and can_save >= 100:
            C += 1
    return C


def main():
    grid, S, E = parse()
    # steps = search(grid, *S, *E)
    # print(f"Part 1: {cheat(grid, *S, *E, steps)}")
    print(f"Part 1: {smart_cheat(grid, *S, time_to_cheat=2)}")
    print(f"Part 2:{smart_cheat(grid, *S, time_to_cheat=20)}")


if __name__ == "__main__":
    main()
