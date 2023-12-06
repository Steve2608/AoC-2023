import math

from timing_util import Timing


def get_data(content: str) -> tuple[list[int], list[int]]:
    times, distances = content.split("\n")
    times = times[len("Time:") :].strip().split()
    distances = distances[len("Distance:") :].strip().split()
    return list(map(int, times)), list(map(int, distances))


def solve_closed_form(time: int, distance: int) -> tuple[int, int]:
    discriminant = math.sqrt(time**2 - 4 * distance)
    w_time_min = math.floor((time - discriminant) / 2 + 1)
    w_time_max = math.ceil((time + discriminant) / 2 - 1)
    return w_time_min, w_time_max


def part1(data: tuple[list[int], list[int]]) -> int:
    prod = 1
    for time, distance in zip(*data):
        w_time_min, w_time_max = solve_closed_form(time, distance)
        prod *= w_time_max - w_time_min + 1
    return prod


def part2(data: tuple[list[int], list[int]]) -> int:
    time, distance = (int("".join(map(str, d))) for d in data)

    w_time_min, w_time_max = solve_closed_form(time, distance)
    return w_time_max - w_time_min + 1


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day06.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
