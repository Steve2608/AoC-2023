import collections

from timing_util import Timing


def get_data(content: str) -> tuple[tuple[int, int], list[list[str]]]:
    grid = [list(line) for line in content.splitlines()]
    for x, line in enumerate(grid):
        if "S" in line:
            y = line.index("S")
            line[y] = starting_pipe(start := (x, y), grid)
            return start, grid
    raise ValueError


def starting_pipe(start: tuple[int, int], grid: list[list[str]]):
    x, y = start
    up = x - 1 >= 0 and grid[x - 1][y] in "|F7"
    down = x + 1 < len(grid) and grid[x + 1][y] in "|LJ"
    left = y - 1 >= 0 and grid[x][y - 1] in "-LF"
    right = y + 1 < len(grid[x]) and grid[x][y + 1] in "-J7"

    match (up, down, left, right):
        case (True, True, False, False):
            return "|"
        case (True, False, True, False):
            return "J"
        case (True, False, False, True):
            return "L"
        case (False, True, True, False):
            return "7"
        case (False, True, False, True):
            return "F"
        case (False, False, True, True):
            return "-"
        case _:
            raise ValueError(f"Illegal pipe required for {(up, down, left, right)}")


def is_connected(src: tuple[int, int], dst: tuple[int, int], grid: list[list[str]]) -> bool:
    x_dst, y_dst = dst
    dst_pipe = grid[x_dst][y_dst]
    if dst_pipe == ".":
        # can never connect to "."
        return False

    x_src, y_src = src
    src_pipe = grid[x_src][y_src]

    if x_src == x_dst:
        # right
        if y_src + 1 == y_dst:
            return src_pipe in "-LF" and dst_pipe in "7J-"
        # left
        if y_src - 1 == y_dst:
            return src_pipe in "7J-" and dst_pipe in "-LF"
    elif y_src == y_dst:
        # down
        if x_src + 1 == x_dst:
            return src_pipe in "F7|" and dst_pipe in "LJ|"
        # up
        if x_src - 1 == x_dst:
            return src_pipe in "LJ|" and dst_pipe in "F7|"
    return False


def trace_path(start: tuple[int, int], grid: list[list[str]]) -> list[tuple[int, int]]:
    M, N = len(grid), len(grid[0])
    visited = set()
    path = []
    curr = start
    while curr not in visited:
        visited.add(curr)
        path.append(curr)

        x, y = curr
        for i, j in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if i < 0 or i >= M or j < 0 or j >= N:
                continue

            if (step := (i, j)) not in visited and is_connected(curr, step, grid):
                curr = step
                # we can only ever connect to one tile
                break

    return path


def part1(data: tuple[tuple[int, int], list[list[str]]]) -> int:
    start, grid = data
    path = trace_path(start, grid)
    return len(path) // 2


def set_tile(x: int, y: int, tile: str, zoomed: list[list[str]]):
    match tile:
        case "|":
            fill_in = [
                [" ", "x", " "],
                [" ", "x", " "],
                [" ", "x", " "],
            ]
        case "-":
            fill_in = [
                [" ", " ", " "],
                ["x", "x", "x"],
                [" ", " ", " "],
            ]
        case "7":
            fill_in = [
                [" ", " ", " "],
                ["x", "x", " "],
                [" ", "x", " "],
            ]
        case "F":
            fill_in = [
                [" ", " ", " "],
                [" ", "x", "x"],
                [" ", "x", " "],
            ]
        case "J":
            fill_in = [
                [" ", "x", " "],
                ["x", "x", " "],
                [" ", " ", " "],
            ]
        case "L":
            fill_in = [
                [" ", "x", " "],
                [" ", "x", "x"],
                [" ", " ", " "],
            ]
        case _:
            raise ValueError

    for i, fill in enumerate(fill_in):
        zoomed[x * 3 + i][y * 3 : (y + 1) * 3] = fill


def init_zoomed(grid: list[list[str]], path: list[tuple[int, int]]) -> list[list[str]]:
    # replace every tile with a 3-by-3 "zoomed in" tile
    zoomed = [[" " for _ in range(len(grid[0] * 3))] for _ in range(len(grid) * 3)]
    for x, y in path:
        set_tile(x, y, grid[x][y], zoomed)
    return zoomed


def is_inside(
    start: tuple[int, int],
    zoomed: list[list[str]],
    known_inside: set[tuple[int, int]],
    known_outside: set[tuple[int, int]],
) -> bool:
    if start in known_inside:
        return True
    if start in known_outside:
        return False

    M, N = len(zoomed), len(zoomed[0])
    visited = set()
    fringe = collections.deque([start])
    while fringe:
        curr = fringe.popleft()

        x, y = curr
        for i, j in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (step := (i, j)) in known_outside or i < 0 or i >= M or j < 0 or j >= N:
                known_outside.update(visited)
                return False

            # cannot walk over pipes
            if zoomed[i][j] == "x":
                continue

            if step in known_inside:
                known_inside.update(visited)
                return True

            if step not in visited:
                fringe.append(step)
                visited.add(step)

    known_inside.update(visited)
    return True


def count_inside(
    grid: list[list[str]],
    zoomed: list[list[str]],
    path: set[tuple[int, int]],
) -> int:
    n = 0
    known_outside = set()
    known_inside = set()
    for x, line in enumerate(grid):
        for y, _ in enumerate(line):
            if (x, y) not in path:
                n += is_inside((x * 3 + 1, y * 3 + 1), zoomed, known_outside, known_inside)

    return n


def part2(data: tuple[tuple[int, int], list[list[str]]]) -> int:
    start, grid = data

    path = trace_path(start, grid)
    zoomed = init_zoomed(grid, path)

    return count_inside(grid, zoomed, set(path))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day10.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
