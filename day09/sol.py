from timing_util import Timing


def get_data(content: str) -> list[list[int]]:
    return list(list(map(int, line.split())) for line in content.splitlines())


def differences(sequence: list[int]) -> list[int]:
    return [b - a for a, b in zip(sequence[:-1], sequence[1:])]


def part1(data: list[list[int]]) -> int:
    def next_in_sequence(sequence: list[int]):
        if not any(sequence):
            return 0
        return sequence[-1] + next_in_sequence(differences(sequence))

    return sum(map(next_in_sequence, data))


def part2(data: list[list[int]]) -> int:
    def next_in_sequence(sequence: list[int]):
        if not any(sequence):
            return 0
        return sequence[0] - next_in_sequence(differences(sequence))

    return sum(map(next_in_sequence, data))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day09.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
