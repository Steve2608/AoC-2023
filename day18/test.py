import unittest

from day18.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(62, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(952408144115, p2)


if __name__ == "__main__":
    unittest.main()
