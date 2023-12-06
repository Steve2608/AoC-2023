import math

from timing_util import Timing

Race = tuple[int, int]


def get_data(content: str) -> list[Race]:
    times, distances = content.split("\n")
    times = times[len("Time:") :].strip().split()
    distances = distances[len("Distance:") :].strip().split()
    return list(zip(map(int, times), map(int, distances)))


def solve_closed_form(time: int, distance: int) -> tuple[int, int]:
    discriminant = math.sqrt(time**2 - 4 * distance)
    w_time_min = math.floor((time - discriminant) / 2 + 1)
    w_time_max = math.ceil((time + discriminant) / 2 - 1)
    return w_time_min, w_time_max


def part1(data: list[Race]) -> int:
    prod = 1
    for time, distance in data:
        w_time_min, w_time_max = solve_closed_form(time, distance)
        prod *= w_time_max - w_time_min + 1
    return prod


def part2(data: list[Race]) -> int:
    time = int("".join(map(str, (td[0] for td in data))))
    distance = int("".join(map(str, (td[1] for td in data))))

    w_time_min, w_time_max = solve_closed_form(time, distance)
    return w_time_max - w_time_min + 1


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day06.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
