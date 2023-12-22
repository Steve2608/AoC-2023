import unittest

from day22.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(5, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(7, p2)


if __name__ == "__main__":
    unittest.main()
