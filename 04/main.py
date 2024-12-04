import fileinput


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    return grid


def get_candidates(grid, row, col):
    H, W = len(grid), len(grid[0])
    candidates = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            candidate = []
            for i in range(4):
                r = row + (i * dr)
                c = col + (i * dc)
                if 0 <= r < H and 0 <= c < W:
                    candidate.append(grid[r][c])
                else:
                    break
            else:
                candidates.append("".join(candidate))
    return candidates


def search(grid):
    count = 0
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "X":
                candidates = get_candidates(grid, row, col)
                count += sum(word == "XMAS" for word in candidates)
    return count


def get_cross(grid, row, col):
    H, W = len(grid), len(grid[0])
    cross = []
    for dr, dc in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            cross.append(grid[row + dr][col + dc])
        else:
            return []
    return cross


def search_cross(grid):
    count = 0
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "A":
                cross = get_cross(grid, row, col)
                if not cross:
                    continue

                if cross[0] + cross[1] in ("MS", "SM") and cross[2] + cross[3] in (
                    "MS",
                    "SM",
                ):
                    count += 1
    return count


def main():
    grid = parse()
    count = search(grid)
    print(f"Part 1: {count}")

    count = search_cross(grid)
    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
