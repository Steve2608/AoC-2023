import copy

from timing_util import Timing


def get_data(data: str) -> list[list[str]]:
    return [list(line) for line in data.split("\n")]


def step_north(state: list[list[str]]):
    has_changed = True
    while has_changed:
        has_changed = False
        for y, row in enumerate(state[1:], 1):
            for x, val in enumerate(row):
                if val == "O" and state[y - 1][x] == ".":
                    i = y - 1
                    while i > 0 and state[i - 1][x] == ".":
                        i -= 1

                    state[i][x] = "O"
                    state[y][x] = "."
                    has_changed = True


def score(state: list[list[str]]) -> int:
    s = 0
    for score, row in enumerate(reversed(state), 1):
        for val in row:
            if val == "O":
                s += score
    return s


def part1(data: list[list[str]]) -> int:
    step_north(state := copy.deepcopy(data))
    return score(state)


def step_west(state: list[list[str]]):
    has_changed = True
    while has_changed:
        has_changed = False
        for y, row in enumerate(state):
            for x, val in reversed(list(enumerate(row[1:], 1))):
                if val == "O" and state[y][x - 1] == ".":
                    i = x - 1
                    while i > 0 and state[y][i - 1] == ".":
                        i -= 1

                    state[y][x - 1] = "O"
                    state[y][x] = "."
                    has_changed = True


def step_south(state: list[list[str]]):
    has_changed = True
    while has_changed:
        has_changed = False
        for y, row in reversed(list(enumerate(state[:-1]))):
            for x, val in enumerate(row):
                if val == "O" and state[y + 1][x] == ".":
                    i = y + 1
                    while i < len(state) - 1 and state[i + 1][x] == ".":
                        i += 1

                    state[i][x] = "O"
                    state[y][x] = "."
                    has_changed = True


def step_east(state: list[list[str]]):
    has_changed = True
    while has_changed:
        has_changed = False
        for y, row in enumerate(state):
            for x, val in enumerate(row[:-1]):
                if val == "O" and state[y][x + 1] == ".":
                    i = x + 1
                    while i < len(row) - 1 and state[y][i + 1] == ".":
                        i += 1

                    state[y][i] = "O"
                    state[y][x] = "."
                    has_changed = True


def cycle(state: list[list[str]]):
    step_north(state)
    step_west(state)
    step_south(state)
    step_east(state)


def to_hashable(data: list[list[str]]) -> str:
    return "".join(["".join(row) for row in data])


def part2(data: list[list[str]], n_cycles: int = 1_000_000_000) -> int:
    state_to_iteration = {}
    iteration_to_state = []

    i, state = 0, data
    while (hashed := to_hashable(state)) not in state_to_iteration:
        state_to_iteration[hashed] = i
        iteration_to_state.append(copy.deepcopy(state))

        cycle(state)
        i += 1

    first_reached = state_to_iteration[to_hashable(state)]
    cycles_remaining = n_cycles - first_reached
    cycles_remaining %= i - first_reached

    state = iteration_to_state[first_reached + cycles_remaining]
    return score(state)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day14.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
