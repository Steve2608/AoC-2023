import itertools as it
from functools import partial

from timing_util import Timing


def get_data(content: str) -> tuple[set[tuple[int, int]], list[int], list[int]]:
    grid = content.split("\n")

    galaxies = set()
    for x, line in enumerate(grid):
        for y, c in enumerate(line):
            if c == "#":
                galaxies.add((x, y))

    expansion_rows = []
    for x, line in enumerate(grid):
        if "#" not in line:
            expansion_rows.append(x)

    expansion_cols = []
    for y in range(len(grid[0])):
        if all(line[y] != "#" for line in grid):
            expansion_cols.append(y)

    return galaxies, expansion_rows, expansion_cols


def manhattan_distance(
    p1: tuple[int, int],
    p2: tuple[int, int],
    expansion_rows: list[int],
    expansion_cols: list[int],
    expansion_size: int,
) -> int:
    src_x, src_y = p1
    dst_x, dst_y = p2

    min_x = src_x if src_x < dst_x else dst_x
    max_x = src_x if src_x > dst_x else dst_x
    min_y = src_y if src_y < dst_y else dst_y
    max_y = src_y if src_y > dst_y else dst_y

    n_rows = 0
    for row in expansion_rows:
        if min_x < row < max_x:
            n_rows += 1

    n_cols = 0
    for col in expansion_cols:
        if min_y < col < max_y:
            n_cols += 1

    return (max_x - min_x) + (max_y - min_y) + (n_rows + n_cols) * expansion_size


def sol(data: tuple[set[tuple[int, int]], list[int], list[int]], expansion_size: int) -> int:
    galaxies, expansion_rows, expansion_cols = data
    return sum(
        manhattan_distance(g1, g2, expansion_rows, expansion_cols, expansion_size - 1)
        for g1, g2 in it.combinations(galaxies, 2)
    )


part1 = partial(sol, expansion_size=2)
part2 = partial(sol, expansion_size=1_000_000)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day11.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
