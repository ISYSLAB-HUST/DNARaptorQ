import unittest
from DNARaptorQ.lfsr import *


class TestLfsr(unittest.TestCase):
    def setUp(self) -> None:
        self.len_payload = 32
        self.seed = 111
        self.ps = [0, 222, 1, 188, 3, 120, 6, 240, 13, 224, 27, 192, 55, 128, 111, 0, 222, 0, 188, 45, 120, 119, 240,
                   238, 225, 241, 195, 207, 135, 179, 15, 75]

    def test_pseudo_random(self):
        self.assertEqual(pseudo_random(self.seed, self.len_payload), self.ps)


if __name__ == '__main__':
    unittest.main()
