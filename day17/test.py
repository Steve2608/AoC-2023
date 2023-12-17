import unittest

from day17.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
        )

        self.data2 = get_data(
            r"""111111111111
999999999991
999999999991
999999999991
999999999991"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(102, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(94, p2)
        p2 = part2(self.data2)
        self.assertEqual(71, p2)


if __name__ == "__main__":
    unittest.main()
