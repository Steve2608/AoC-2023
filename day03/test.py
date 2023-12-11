import unittest

from day03.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(4361, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(467835, p2)


if __name__ == "__main__":
    unittest.main()
