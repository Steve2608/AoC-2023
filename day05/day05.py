import dataclasses

from timing_util import Timing


@dataclasses.dataclass(slots=True)
class Map:
    seed_to_soil_map: list[tuple[int, int, int]]
    soil_to_fertilizer_map: list[tuple[int, int, int]]
    fertilizer_to_water_map: list[tuple[int, int, int]]
    water_to_light_map: list[tuple[int, int, int]]
    light_to_temperature_map: list[tuple[int, int, int]]
    temperature_to_humidity_map: list[tuple[int, int, int]]
    humidity_to_location_map: list[tuple[int, int, int]]

    def __post_init__(self) -> None:
        pass

    def seed_to_soil(self, seed: int) -> int:
        for dst, src, rng in self.seed_to_soil_map:
            if src <= seed < src + rng:
                return dst + (seed - src)
        return seed

    def soil_to_seed(self, soil: int) -> int:
        for dst, src, rng in self.seed_to_soil_map:
            if dst <= soil < dst + rng:
                return src + (soil - dst)
        return soil

    def soil_to_fertilizer(self, soil: int) -> int:
        for dst, src, rng in self.soil_to_fertilizer_map:
            if src <= soil < src + rng:
                return dst + (soil - src)
        return soil

    def fertilizer_to_soil(self, fertilizer: int) -> int:
        for dst, src, rng in self.soil_to_fertilizer_map:
            if dst <= fertilizer < dst + rng:
                return src + (fertilizer - dst)
        return fertilizer

    def fertilizer_to_water(self, fertilizer: int) -> int:
        for dst, src, rng in self.fertilizer_to_water_map:
            if src <= fertilizer < src + rng:
                return dst + (fertilizer - src)
        return fertilizer

    def water_to_fertilizer(self, water: int) -> int:
        for dst, src, rng in self.fertilizer_to_water_map:
            if dst <= water < dst + rng:
                return src + (water - dst)
        return water

    def water_to_light(self, water: int) -> int:
        for dst, src, rng in self.water_to_light_map:
            if src <= water < src + rng:
                return dst + (water - src)
        return water

    def light_to_water(self, light: int) -> int:
        for dst, src, rng in self.water_to_light_map:
            if dst <= light < dst + rng:
                return src + (light - dst)
        return light

    def light_to_temperature(self, light: int) -> int:
        for dst, src, rng in self.light_to_temperature_map:
            if src <= light < src + rng:
                return dst + (light - src)
        return light

    def temperature_to_light(self, temperature: int) -> int:
        for dst, src, rng in self.light_to_temperature_map:
            if dst <= temperature < dst + rng:
                return src + (temperature - dst)
        return temperature

    def temperature_to_humidity(self, temperature: int) -> int:
        for dst, src, rng in self.temperature_to_humidity_map:
            if src <= temperature < src + rng:
                return dst + (temperature - src)
        return temperature

    def humidity_to_temperature(self, humidity: int) -> int:
        for dst, src, rng in self.temperature_to_humidity_map:
            if dst <= humidity < dst + rng:
                return src + (humidity - dst)
        return humidity

    def humidity_to_location(self, humidity: int) -> int:
        for dst, src, rng in self.humidity_to_location_map:
            if src <= humidity < src + rng:
                return dst + (humidity - src)
        return humidity

    def location_to_humidity(self, location: int) -> int:
        for dst, src, rng in self.humidity_to_location_map:
            if dst <= location < dst + rng:
                return src + (location - dst)
        return location


def get_data(content: str) -> tuple[list[int], Map]:
    lines = list(filter(bool, content.split("\n")))
    seeds = list(map(int, lines[0][len("seeds: ") :].split()))

    seed_to_soil_map = []
    soil_to_fertilizer_map = []
    fertilizer_to_water_map = []
    water_to_light_map = []
    light_to_temperature_map = []
    temperature_to_humidity_map = []
    humidity_to_location_map = []

    for line in lines[1:]:
        match line:
            case "seed-to-soil map:":
                target = seed_to_soil_map
            case "soil-to-fertilizer map:":
                target = soil_to_fertilizer_map
            case "fertilizer-to-water map:":
                target = fertilizer_to_water_map
            case "water-to-light map:":
                target = water_to_light_map
            case "light-to-temperature map:":
                target = light_to_temperature_map
            case "temperature-to-humidity map:":
                target = temperature_to_humidity_map
            case "humidity-to-location map:":
                target = humidity_to_location_map
            case _:
                target.append(tuple(map(int, line.split())))

    return (
        seeds,
        Map(
            seed_to_soil_map,
            soil_to_fertilizer_map,
            fertilizer_to_water_map,
            water_to_light_map,
            light_to_temperature_map,
            temperature_to_humidity_map,
            humidity_to_location_map,
        ),
    )


def part1(data: tuple[list[int], Map]) -> int:
    def seed_to_location(seed: int) -> int:
        soil = m.seed_to_soil(seed)
        fertilizer = m.soil_to_fertilizer(soil)
        water = m.fertilizer_to_water(fertilizer)
        light = m.water_to_light(water)
        temperature = m.light_to_temperature(light)
        humidity = m.temperature_to_humidity(temperature)
        location = m.humidity_to_location(humidity)
        return location

    seeds, m = data
    return min(map(seed_to_location, seeds))


def part2(data: tuple[list[int], Map]) -> int:
    def location_to_seed(seed: int) -> int:
        humidity = m.location_to_humidity(seed)
        temperature = m.humidity_to_temperature(humidity)
        light = m.temperature_to_light(temperature)
        water = m.light_to_water(light)
        fertilizer = m.water_to_fertilizer(water)
        soil = m.fertilizer_to_soil(fertilizer)
        seed = m.soil_to_seed(soil)
        return seed

    def count(start: int):
        i = start
        while True:
            yield i
            i += 1

    seeds, m = data

    for loc in count(0):
        seed = location_to_seed(loc)
        for start, l in zip(seeds[::2], seeds[1::2]):
            if start <= seed < start + l:
                return loc
    # TODO: 104070862


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day05.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
