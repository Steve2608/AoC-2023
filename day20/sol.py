import copy
import dataclasses as dc
import itertools as it
import math
from collections import deque

from timing_util import Timing


@dc.dataclass
class Module:
    name: str
    modules: list["Module"] = dc.field(default_factory=list)

    def __call__(self, high: bool, src: str) -> list[tuple["Module", bool, str]]:
        return [(module, high, self.name) for module in self.modules]


@dc.dataclass
class Button(Module):
    def __call__(self, high: bool, src: str) -> list[tuple["Module", bool, str]]:
        return super().__call__(high=False, src=self.name)


@dc.dataclass
class FlipFlop(Module):
    state: bool = False

    def __call__(self, high: bool, src: str) -> list[tuple["Module", bool, str]]:
        if high:
            return []
        else:
            self.state = not self.state
            return super().__call__(high=self.state, src=self.name)


@dc.dataclass
class NAND(Module):
    inputs: dict[str, bool] = dc.field(default_factory=dict)

    def __call__(self, high: bool, src: str) -> list[tuple["Module", bool, str]]:
        self.inputs[src] = high
        if all(self.inputs.values()):
            return super().__call__(high=False, src=self.name)
        return super().__call__(high=True, src=self.name)


def get_data(data: str) -> dict[str, Module]:
    modules = {}
    conjunctions = {}
    for line in data.split("\n"):
        name, inputs = line.split(" -> ")
        if name.startswith("%"):
            module_type = FlipFlop
            name = name[1:]
        elif name.startswith("&"):
            module_type = NAND
            name = name[1:]
            conjunctions[name] = []
        elif name == "broadcaster":
            module_type = Module
            name = "broadcaster"
        else:
            raise ValueError(f"Unknown module type: {name}")

        modules[name] = module_type(name=name)

    for line in data.split("\n"):
        name, inputs = line.split(" -> ")
        inputs = inputs.split(", ")
        if name.startswith("%"):
            name = name[1:]
        elif name.startswith("&"):
            name = name[1:]
        elif name == "broadcaster":
            name = "broadcaster"
        else:
            raise ValueError(f"Unknown module type: {name}")

        for inp in inputs:
            if inp not in modules:
                modules[inp] = Module(name=inp)
            if inp in conjunctions:
                conjunctions[inp].append(name)

        modules[name].modules = [modules[inp] for inp in inputs]

    for conj, inputs in conjunctions.items():
        modules[conj].inputs = {name: False for name in inputs}

    return modules


def part1(data: dict[str, Module]) -> int:
    data = copy.deepcopy(data)
    broadcaster = data["broadcaster"]
    high_count = 0
    low_count = 0
    for _ in range(1_000):
        queue: deque[tuple[Module, bool, str]] = deque([(broadcaster, False, "button")])
        while queue:
            module, high, src = queue.popleft()

            high_count += high
            low_count += not high

            queue.extend(module(high=high, src=src))

    return high_count * low_count


def part2(data: dict[str, Module], last_module: str = "rx") -> int:
    def find_last_NAND(data: dict[str, Module], last_module: str) -> dict[str, int]:
        for module in data.values():
            for m in module.modules:
                if m.name == last_module and isinstance(module, NAND):
                    return dict(zip(module.inputs, it.repeat(0)))
        raise ValueError("No solution found")

    NAND_inputs = find_last_NAND(data := copy.deepcopy(data), last_module)
    broadcaster = data["broadcaster"]
    for i in it.count(1):
        queue: deque[tuple[Module, bool, str]] = deque([(broadcaster, False, "button")])
        while queue:
            module, high, src = queue.popleft()
            if (n := module.name) in NAND_inputs and not high:
                # assign period of input for last conjunction
                if not NAND_inputs[n]:
                    NAND_inputs[n] = i

            # if we found the period of all conjunctions
            # return least common multiple of all periods
            if all(v := NAND_inputs.values()):
                return math.lcm(*v)

            queue.extend(module(high=high, src=src))
    raise ValueError("No solution found")


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day20.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
