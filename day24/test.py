import unittest

from day24.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data, x_min=7, y_min=7, x_max=27, y_max=27)
        self.assertEqual(2, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(47, p2)


if __name__ == "__main__":
    unittest.main()
