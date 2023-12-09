import unittest

from day09 import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(114, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(2, p2)


if __name__ == "__main__":
    unittest.main()
