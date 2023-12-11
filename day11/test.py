import unittest

from day11.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(374, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data, expansion_size=10)
        self.assertEqual(1_030, p2)
        p2 = part2(self.data, expansion_size=100)
        self.assertEqual(8_410, p2)


if __name__ == "__main__":
    unittest.main()
