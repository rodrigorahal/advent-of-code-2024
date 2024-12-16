import fileinput
import heapq


def parse():
    grid = [line.strip() for line in fileinput.input()]
    S, E = None, None
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "S":
                S = (row, col)
            if char == "E":
                E = (row, col)
    return grid, S, E


def dijkstra(grid, srow, scol, erow, ecol, remove=None):
    if not remove:
        remove = set()
    H, W = len(grid), len(grid[0])
    queue = []
    (cost, row, col, dr, dc, path) = (0, srow, scol, 0, 1, ((srow, scol),))
    heapq.heappush(queue, (cost, row, col, dr, dc, path))
    seen = set()

    while queue:
        cost, row, col, dr, dc, path = heapq.heappop(queue)

        if (row, col, dr, dc) in seen:
            continue
        seen.add((row, col, dr, dc))

        if (row, col) == (erow, ecol):
            return cost, path

        for ndr, ndc, nc in [(dr, dc, 1), (-dc, -dr, 1000 + 1), (dc, dr, 1000 + 1)]:
            nrow, ncol = row + ndr, col + ndc
            if (
                0 <= nrow < H
                and 0 <= ncol < W
                and grid[nrow][ncol] != "#"
                and (nrow, col) not in remove
            ):
                heapq.heappush(
                    queue, (cost + nc, nrow, ncol, ndr, ndc, path + ((nrow, ncol),))
                )
    return -1, ()


def nodes(grid, srow, scol, erow, ecol, mincost, minpath):
    N = set()
    for row, col in minpath:
        if (row, col) not in [(srow, scol), (erow, ecol)]:
            remove = set([(row, col)])
            cost, path = dijkstra(grid, srow, scol, erow, ecol, remove)
            if cost == mincost:
                N.update(path)
    return len(N)


def main():
    grid, S, E = parse()
    mincost, path = dijkstra(grid, *S, *E)
    print(f"Part 1: {mincost}")
    print(f"Part 2: {nodes(grid, *S, *E, mincost, path)}")


if __name__ == "__main__":
    main()
