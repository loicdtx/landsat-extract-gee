from geextract import get_date
import unittest
from datetime import date

class TestFilenameParsing(unittest.TestCase):
    def test_date_extraction(self):
        f1 = 'LC81970292013106'
        d1 = date(2013, 4, 16)
        f2 = 'LANDSAT/LE07/C01/T1_SR/LE07_023039_20000604'
        d2 = date(2000, 6, 4)
        f3 = 'LE07_023039_20000604'
        d3 = date(2000, 6, 4)

        self.assertEqual(get_date(f1), d1)
        self.assertEqual(get_date(f2), d2)
        self.assertEqual(get_date(f3), d3)
