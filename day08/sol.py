import itertools as it
import math
from functools import partial
from typing import Callable

from timing_util import Timing


def get_data(content: str) -> tuple[str, dict[str, tuple[str, str]]]:
    directions, lines = content.split("\n\n")
    # node = (left, right)
    # ABC = (DEF, GHI)
    nodes = {line[:3]: (line[7:10], line[12:15]) for line in lines.splitlines()}

    return directions, nodes


def period_length(
    curr: str,
    directions: str,
    nodes: dict[str, tuple[str, str]],
    is_end: Callable[[str], bool],
):
    for i, direction in enumerate(it.cycle(directions)):
        if is_end(curr):
            return i

        # coerce boolean to index: false -> left; true -> right
        curr = nodes[curr][direction == "R"]
    raise ValueError


def part1(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    def is_end(node: str) -> bool:
        return node == "ZZZ"

    directions, nodes = data
    return period_length("AAA", directions, nodes, is_end)


def part2(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    def is_end(node: str) -> bool:
        return node[-1] == "Z"

    directions, nodes = data
    period = partial(period_length, directions=directions, nodes=nodes, is_end=is_end)

    return math.lcm(*map(period, (node for node in nodes if node[-1] == "A")))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day08.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
