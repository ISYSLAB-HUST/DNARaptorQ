import unittest

from DNARaptorQ.rs import *


class TestRs(unittest.TestCase):
    def setUp(self) -> None:
        _rs = InnerRScode(2)
        self.enc = _rs.encode([1, 2, 3])
        self.dec = _rs.decode(self.enc)

    def test_RScode(self):
        self.assertEqual(list(self.dec)[:-2], [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
