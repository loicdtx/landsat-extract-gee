from geextract import get_date, date_append
import unittest
from datetime import date


dict_list = [{'id': "LT50200461986040", 'B1': 12, 'B2': 23},
             {'id': "LT50200461986072", 'B1': 45, 'B2': 54},
             {'id': "LT50200461986104", 'B1': None, 'B2': 54},
             {'id': "LT50200461986232", 'B1': None, 'B2': None},
             {'id': "LT50200461986296", 'B1': 45, 'B2': 54},
]

dict_list_with_time = [{'B1': 12,
                        'B2': 23,
                        'id': 'LT50200461986040',
                        'time': date(1986, 2, 9)},
                       {'B1': 45,
                        'B2': 54,
                        'id': 'LT50200461986072',
                        'time': date(1986, 3, 13)},
                       {'B1': None,
                        'B2': 54,
                        'id': 'LT50200461986104',
                        'time': date(1986, 4, 14)},
                       {'B1': None,
                        'B2': None,
                        'id': 'LT50200461986232',
                        'time': date(1986, 8, 20)},
                       {'B1': 45,
                        'B2': 54,
                        'id': 'LT50200461986296',
                        'time': date(1986, 10, 23)}]

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


class TestUtils(unittest.TestCase):
    def test_date_append(self):
        self.assertEqual(date_append(dict_list), dict_list_with_time)

