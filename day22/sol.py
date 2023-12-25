import copy

from timing_util import Timing

Point3D = tuple[int, int, int]


def get_data(data: str) -> list[tuple[Point3D, Point3D]]:
    bricks = []
    for line in data.splitlines():
        start, end = line.split("~")
        bricks.append((tuple(map(int, start.split(","))), tuple(map(int, end.split(",")))))
    return bricks


def simulate_bricks(
    data: list[tuple[Point3D, Point3D]]
) -> tuple[list[set[Point3D]], list[set[int]]]:
    bricks: list[set[Point3D]] = [
        {(x, y, z) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1) for z in range(z1, z2 + 1)}
        for (x1, y1, z1), (x2, y2, z2) in data
    ]

    locations = set.union(*bricks)
    dropped = True
    while dropped:
        dropped = False
        for i, brick in enumerate(bricks):
            # remove brick to test if it can fall
            locations.difference_update(brick)
            fallen = {(x, y, z - 1) for x, y, z in brick}
            if all(f not in locations for f in fallen) and all(z > 1 for _, _, z in brick):
                bricks[i] = fallen
                locations.update(fallen)
                dropped = True
            else:
                # add brick back in if it can't
                locations.update(brick)

    sitting_on = [
        {
            j
            for j, other_brick in enumerate(bricks)
            if i != j and any((x, y, z - 1) in other_brick for x, y, z in brick)
        }
        for i, brick in enumerate(bricks)
    ]

    return bricks, sitting_on


def part1(data: list[tuple[Point3D, Point3D]]) -> int:
    bricks, sitting_on = simulate_bricks(data)

    return len(bricks) - len({v.pop() for v in sitting_on if len(v) == 1})


def part2(data: list[tuple[Point3D, Point3D]]) -> int:
    def n_falling_if_removed(remove: set[int]) -> int:
        unsupported = {
            k
            for k, v in enumerate(sitting_on)
            if not (k in remove or k in on_floor) and not v.difference(remove)
        }
        if unsupported:
            return len(unsupported) + n_falling_if_removed(remove | unsupported)
        return 0

    bricks, sitting_on = simulate_bricks(data)

    on_floor = {k for k, v in enumerate(sitting_on) if not v}

    return sum(n_falling_if_removed({i}) for i in range(len(bricks)))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day22.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
