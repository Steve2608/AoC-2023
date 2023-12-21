from collections import deque

from timing_util import Timing

Point2D = tuple[int, int]


def get_data(data: str) -> tuple[Point2D, list[str]]:
    grid = data.split("\n")
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                grid[i] = grid[i].replace("S", ".")
                return (i, j), grid
    raise ValueError


# https://github.com/dancarmoz/AoC2023/blob/main/day21.py
# used to be a "basic" bfs, but changed it to make part2 work
def cumbfs(grid: list[str], start: Point2D, n_steps: int) -> list[int]:
    X, Y = len(grid), len(grid[0])
    sizes = [0, 1]
    prev, curr = set(), {start}
    for _ in range(n_steps):
        prev, curr = curr, set(
            [
                (ii, jj)
                for i, j in curr
                for ii, jj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                if grid[ii % X][jj % Y] == "." and (ii, jj) not in prev
            ]
        )
        sizes.append(sizes[-2] + len(curr))
    return sizes[1:]


def part1(data: tuple[Point2D, list[str]], n_steps: int = 64) -> int:
    start, grid = data
    return cumbfs(grid, start, n_steps)[-1]


def part2(data: tuple[Point2D, list[str]], n_steps: int = 26501365) -> int:
    start, grid = data
    N = len(grid)

    # didn't even get close to solving this one myself, barely makes sense in hindsight
    # https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # reachable spaces grow like a rhombus with the corner points = start shifted up/down/left/right
    # since there's no obstacles in the same column / row as the start
    # area has to grow quadratically

    # also only works since the grid is a square, the start is in the middle of the square
    # and n_steps is a multiple of N + N//2

    # the amount of reachable spaces after n steps is a quadratic function
    # f(n) = a*n^2 + b*n + C
    sizes = cumbfs(grid, start, n_steps=(n_steps % N) + 2 * N)[n_steps % N :: N]

    # fitting the quadratic
    diff = [b - a for a, b in zip(sizes[:-1], sizes[1:])]
    diff_diff = [b - a for a, b in zip(diff[:-1], diff[1:])]
    a, b, c = diff_diff[0], diff[0], sizes[0]

    # solving the quadratic
    x = n_steps // N
    return a * x * (x - 1) // 2 + b * x + c


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day21.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
