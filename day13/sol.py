import copy
import itertools as it

from timing_util import Timing


def get_data(content: str) -> list[list[list[str]]]:
    return [[list(line) for line in chunk.splitlines()] for chunk in content.split("\n\n")]


def is_palindrome(seq1, seq2) -> bool:
    for a, b in zip(seq1, seq2):
        if a != b:
            return False
    return True


def mirror_vertically(chunk: list[list[str]]):
    for i in range(1, len(chunk[0])):
        for line in chunk:
            if not is_palindrome(reversed(line[:i]), line[i:]):
                break
        else:
            yield i


def mirror_horizontally(chunk: list[list[str]]):
    for i in range(1, len(chunk)):
        if is_palindrome(reversed(chunk[:i]), chunk[i:]):
            yield i


def part1(data: list[list[list[str]]]) -> int:
    s = 0
    for chunk in data:
        if v := next(mirror_vertically(chunk), None):
            s += v
        elif h := next(mirror_horizontally(chunk), None):
            s += h * 100
        else:
            raise ValueError

    return s


def smudge(chunk: list[list[str]]) -> int:
    v = next(mirror_vertically(chunk), None)
    h = next(mirror_horizontally(chunk), None)
    chunk_smudge = copy.deepcopy(chunk)
    for i, j in it.product(range(len(chunk)), range(len(chunk[0]))):
        match cache := chunk_smudge[i][j]:
            case "#":
                chunk_smudge[i][j] = "."
            case ".":
                chunk_smudge[i][j] = "#"

        for refl in mirror_vertically(chunk_smudge):
            if refl != v:
                return refl

        for refl in mirror_horizontally(chunk_smudge):
            if refl != h:
                return refl * 100

        # restore original
        chunk_smudge[i][j] = cache
    raise ValueError


def part2(data) -> int:
    return sum(map(smudge, data))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day13.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
