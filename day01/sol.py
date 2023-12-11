from timing_util import Timing


def get_data(content: str) -> list[str]:
    return content.split("\n")


def calibration_number(line: str) -> int:
    def parse_number(line: str) -> int:
        for char in line:
            if char.isdigit():
                return int(char)

    first = parse_number(line)
    last = parse_number(reversed(line))
    return first * 10 + last


def part1(data: list[str]) -> int:
    return sum(map(calibration_number, data))


def calibration_word(line: str) -> int:
    def parse_number_left(line: str) -> int:
        chunk = ""
        for char in line:
            # if we encounter a number: return it immediately
            if char.isdigit():
                return int(char)

            chunk = chunk[-4:] + char

            if len(chunk) >= 3:
                if chunk.endswith("one"):
                    return 1
                if chunk.endswith("two"):
                    return 2
                if chunk.endswith("six"):
                    return 6
            if len(chunk) >= 4:
                if chunk.endswith("four"):
                    return 4
                if chunk.endswith("five"):
                    return 5
                if chunk.endswith("nine"):
                    return 9
            if chunk == "three":
                return 3
            if chunk == "seven":
                return 7
            if chunk == "eight":
                return 8

    def parse_number_right(line: str) -> int:
        chunk = ""
        for char in line:
            # if we encounter a number: return it immediately
            if char.isdigit():
                return int(char)

            chunk = char + chunk[:4]

            if len(chunk) >= 3:
                if chunk.startswith("one"):
                    return 1
                if chunk.startswith("two"):
                    return 2
                if chunk.startswith("six"):
                    return 6
            if len(chunk) >= 4:
                if chunk.startswith("four"):
                    return 4
                if chunk.startswith("five"):
                    return 5
                if chunk.startswith("nine"):
                    return 9
            if chunk == "three":
                return 3
            if chunk == "seven":
                return 7
            if chunk == "eight":
                return 8

    first = parse_number_left(line)
    second = parse_number_right(reversed(line))
    return first * 10 + second


def part2(data: list[str]) -> int:
    return sum(map(calibration_word, data))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day01.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
