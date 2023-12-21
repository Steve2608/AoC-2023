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
    def quadratic_fit(x: list[int], y: list[int]) -> tuple:
        x1, x2, x3 = x
        y1, y2, y3 = y

        denom = (x1 - x2) * (x1 - x3) * (x2 - x3)

        a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
        b = (x3**2 * (y1 - y2) + x2**2 * (y3 - y1) + x1**2 * (y2 - y3)) / denom
        c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom

        return a, b, c

    start, grid = data
    N = len(grid)

    # didn't even get close to solving this one myself, barely makes sense in hindsight
    # https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # reachable spaces grow like a rhombus with the corner points = start shifted up/down/left/right
    # since there's no obstacles in the same column / row as the start
    # area has to grow quadratically

    # the amount of reachable spaces after n steps is a quadratic function
    sizes = cumbfs(grid, start, n_steps=(n_steps % N) + 2 * N)[n_steps % N :: N]

    # fitting the quadratic
    a, b, c = map(int, quadratic_fit([0, 1, 2], sizes))

    # also only works since the grid is a square, the start is in the middle of the square
    # and n_steps is a multiple of N + N//2
    # f(n) = a*n^2 + b*n + c
    def f(x: int) -> int:
        return a * x * x + b * x + c

    return f(n_steps // N)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day21.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
