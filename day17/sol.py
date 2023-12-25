from heapq import heappop as get
from heapq import heappush as put

from timing_util import Timing


def get_data(data: str) -> list[list[int]]:
    return [list(map(int, line)) for line in data.splitlines()]


def ucs(
    curr: tuple[int, int],
    data: list[list[int]],
    min_allowed_repeat: int,
    max_allowed_repeat: int,
) -> int:
    Y, X = len(data), len(data[0])

    visited = set()
    fringe = []
    put(fringe, (0, (curr, "", 0)))
    while fringe:
        cost, state = get(fringe)
        if state in visited:
            continue

        curr, direction, times = state
        if curr == (Y - 1, X - 1):
            if times >= min_allowed_repeat:
                return cost
            continue

        visited.add(state)

        for i, j, step in [(0, 1, "r"), (1, 0, "d"), (0, -1, "l"), (-1, 0, "u")]:
            if direction:
                # has to be the same step as the last one for at least min_allowed_repeat times
                if times < min_allowed_repeat and step != direction:
                    continue

                # no more than max_allowed_repeat repetition possible
                if times == max_allowed_repeat and step == direction:
                    continue

                # cannot turn 180 degrees
                last = direction[-1]
                if last == "r" and step == "l":
                    continue
                if last == "l" and step == "r":
                    continue
                if last == "u" and step == "d":
                    continue
                if last == "d" and step == "u":
                    continue

            y, x = curr[0] + i, curr[1] + j
            if not (0 <= y < Y and 0 <= x < X):
                continue

            if direction == step:
                # continue in the same direction
                put(fringe, (cost + data[y][x], ((y, x), direction, times + 1)))
            else:
                # turn
                put(fringe, (cost + data[y][x], ((y, x), step, 1)))
    raise ValueError


def part1(data: list[list[int]]) -> int:
    return ucs((0, 0), data, min_allowed_repeat=1, max_allowed_repeat=3)


def part2(data: list[list[int]]) -> int:
    return ucs((0, 0), data, min_allowed_repeat=4, max_allowed_repeat=10)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day17.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
