import unittest

from day21.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data, n_steps=1)
        self.assertEqual(2, p1)
        p1 = part1(self.data, n_steps=2)
        self.assertEqual(4, p1)
        p1 = part1(self.data, n_steps=3)
        self.assertEqual(6, p1)
        p1 = part1(self.data, n_steps=6)
        self.assertEqual(16, p1)


if __name__ == "__main__":
    unittest.main()
