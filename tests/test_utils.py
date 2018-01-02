from geextract import get_date, date_append, relabel
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
LE7_dict = [{'B1': 791.0712281921998,
             'B2': 882.609940300239,
             'B3': 989.8438010780741,
             'B4': 2346.717295542807,
             'B5': 2925.630661334263,
             'B7': 1843.7754404295472,
             'id': 'LE07_020046_20170427'},
            {'B1': 421.51089404078505,
             'B2': 624.8624105377779,
             'B3': 551.8283911071643,
             'B4': 3165.8649582950115,
             'B5': 1943.1104732908364,
             'B7': 1008.9000877443359,
             'id': 'LE07_020046_20170630'},
            {'B1': 323.23065242403203,
             'B2': 585.4544074102201,
             'B3': 487.89957540751027,
             'B4': 3455.480794052203,
             'B5': 2173.9796873083665,
             'B7': 1043.4691601011557,
             'id': 'LE07_020046_20170716'}]

LE7_dict_color = [{'blue': 791.0712281921998,
                   'green': 882.609940300239,
                   'red': 989.8438010780741,
                   'nir': 2346.717295542807,
                   'swir1': 2925.630661334263,
                   'swir2': 1843.7754404295472,
                   'id': 'LE07_020046_20170427'},
                  {'blue': 421.51089404078505,
                   'green': 624.8624105377779,
                   'red': 551.8283911071643,
                   'nir': 3165.8649582950115,
                   'swir1': 1943.1104732908364,
                   'swir2': 1008.9000877443359,
                   'id': 'LE07_020046_20170630'},
                  {'blue': 323.23065242403203,
                   'green': 585.4544074102201,
                   'red': 487.89957540751027,
                   'nir': 3455.480794052203,
                   'swir1': 2173.9796873083665,
                   'swir2': 1043.4691601011557,
                   'id': 'LE07_020046_20170716'}]

class TestFilenameParsing(unittest.TestCase):
    def test_date_extraction(self):
        f1 = 'LC81970292013106'
        d1 = date(2013, 4, 16)
        f2 = 'LANDSAT/LE07/C01/T1_SR/LE07_023039_20000604'
        d2 = date(2000, 6, 4)
        f3 = 'LE07_023039_20000604'
        d3 = date(2000, 6, 4)
        f4 = 'S2A_MSIL1C_20170105T013442_N0204_R031_T53NMJ_20170105T013443'

        self.assertEqual(get_date(f1), d1)
        self.assertEqual(get_date(f2), d2)
        self.assertEqual(get_date(f3), d3)
        self.assertRaises(ValueError, get_date, *[f4])


class TestUtils(unittest.TestCase):
    def test_date_append(self):
        self.assertEqual(date_append(dict_list), dict_list_with_time)

    def test_relabel(self):
        self.assertEqual(relabel(LE7_dict, 'LE7'), LE7_dict_color)

