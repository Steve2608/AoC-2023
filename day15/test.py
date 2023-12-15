import unittest

from day15.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(r"""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""")

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(1320, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(145, p2)


if __name__ == "__main__":
    unittest.main()
