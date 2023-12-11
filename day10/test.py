import unittest

from day10.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data1 = get_data(
            r""".....
.S-7.
.|.|.
.L-J.
....."""
        )
        self.data2 = get_data(
            r"""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
        )

        self.data3 = get_data(
            r"""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""
        )

        self.data4 = get_data(
            r"""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data1)
        self.assertEqual(4, p1)
        p1 = part1(self.data2)
        self.assertEqual(8, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data3)
        self.assertEqual(4, p2)
        p2 = part2(self.data4)
        self.assertEqual(10, p2)


if __name__ == "__main__":
    unittest.main()
