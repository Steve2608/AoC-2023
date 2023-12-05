import dataclasses
from typing import Iterator

from timing_util import Timing

Range = tuple[int, int, int]
Interval = tuple[int, int]


@dataclasses.dataclass(slots=True, frozen=True)
class Function:
    ranges: list[Range]

    def apply_one(self, value: int) -> int:
        for dst, src, length in self.ranges:
            if src <= value < src + length:
                return dst + (value - src)
        return value

    def apply_many(self, intervals: list[Interval]) -> Iterator[Interval]:
        for d_start, s_start, length in self.ranges:
            # stop when no intervals left to process
            if not intervals:
                return

            s_end = s_start + length

            # intervals for next step
            intervals_step = []

            for i_start, i_end in intervals:
                # left part of overlap
                if (e := min(i_end, s_start)) > i_start:
                    intervals_step.append((i_start, e))

                # overlap
                if (e := min(i_end, s_end)) > (s := max(i_start, s_start)):
                    i: Interval = d_start + (s - s_start), d_start + (e - s_start)
                    # done with this interval for this mapping
                    yield i

                # right part of overlap
                if i_end > (s := max(i_start, s_end)):
                    intervals_step.append((s, i_end))

            intervals = intervals_step

        # map left-over intervals 1:1 since no range is applicable
        yield from intervals

    def __call__(self, value: int) -> int | Iterator[Interval]:
        if isinstance(value, list):
            return self.apply_many(value)
        elif isinstance(value, int):
            return self.apply_one(value)
        raise ValueError(f"Invalid type: {type(value)}")


def get_data(content: str) -> tuple[list[int], list[Function]]:
    lines = list(filter(bool, content.split("\n")))
    seeds = list(map(int, lines[0][len("seeds: ") :].split()))

    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []

    for line in lines[1:]:
        match line:
            case "seed-to-soil map:":
                target = seed_to_soil
            case "soil-to-fertilizer map:":
                target = soil_to_fertilizer
            case "fertilizer-to-water map:":
                target = fertilizer_to_water
            case "water-to-light map:":
                target = water_to_light
            case "light-to-temperature map:":
                target = light_to_temperature
            case "temperature-to-humidity map:":
                target = temperature_to_humidity
            case "humidity-to-location map:":
                target = humidity_to_location
            case _:
                target.append(Range(map(int, line.split())))
                # sort by src
                target.sort(key=lambda dst_src_len: dst_src_len[1])

    return (
        seeds,
        list(
            map(
                Function,
                [
                    seed_to_soil,
                    soil_to_fertilizer,
                    fertilizer_to_water,
                    water_to_light,
                    light_to_temperature,
                    temperature_to_humidity,
                    humidity_to_location,
                ],
            )
        ),
    )


def part1(data: tuple[list[int], list[Function]]) -> int:
    def seed_to_location(value: int) -> int:
        for func in mapping_functions:
            value = func(value)
        return value

    seeds, mapping_functions = data
    return min(map(seed_to_location, seeds))


def part2(data: tuple[list[int], list[Function]]) -> int:
    def seed_range_to_location(i: Interval) -> int:
        intervals = [i]
        for func in mapping_functions:
            intervals = list(func(intervals))

        return min(start for start, _ in intervals)

    seeds, mapping_functions = data
    # return minimum of all locations
    return min(
        # map to minimum location for range
        map(
            seed_range_to_location,
            map(
                # map (start, len) to (start, end)
                lambda s_l: (s_l[0], s_l[0] + s_l[1]),
                # (start, len)
                zip(
                    seeds[::2],
                    seeds[1::2],
                ),
            ),
        )
    )


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day05.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
