import unittest

from DNARaptorQ.utils import *


class TestUtils(unittest.TestCase):
    def test_IntToFour(self):
        self.assertEqual(IntToFour(0b10110001), "2301")

    def test_BinToDNA(self):
        self.assertEqual(BinToDNA([0b10110001]), "GTAC")

    def test_DNAToBin(self):
        self.assertEqual(DNAToBin("GTAC"), [0b10110001])

    def test_int_to_sixteen(self):
        self.assertEqual(int_to_sixteen(116), "0074")

    def test_sixteen_to_dna(self):
        self.assertEqual(sixteen_to_dna("0074"), "GCTGCTCAACAT")

    def test_dna_to_symbol_id_half(self):
        self.assertEqual(dna_to_symbol_id_half("GCTGCTCAACAT"), 116)

    def test_dna_to_symbol_id(self):
        self.assertEqual(dna_to_symbol_id("GCTGCTGCTGCTGCTGCTACTGAA"), 243)

    def test_symbol_id_to_dna(self):
        self.assertEqual(symbol_id_to_dna(243), "GCTGCTGCTGCTGCTGCTACTGAA")


if __name__ == '__main__':
    unittest.main()
