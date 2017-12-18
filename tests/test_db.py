from geextract import dictlist2sqlite
import unittest
from datetime import datetime
import sqlite3
import tempfile
import os

tmp_dir = tempfile.gettempdir()
db_name = os.path.join(tmp_dir, 'gee_test.sqlite')
if os.path.isfile(db_name):
    os.remove(db_name)
dict_list = [{'id': "LT50200461986040", 'B1': 12, 'B2': 23},
             {'id': "LT50200461986072", 'B1': 45, 'B2': 54},
             {'id': "LT50200461986104", 'B1': None, 'B2': 54},
             {'id': "LT50200461986232", 'B1': None, 'B2': None},
             {'id': "LT50200461986296", 'B1': 45, 'B2': 54},
]

class TestDatabase(unittest.TestCase):
    def test_insert(self):
        dictlist2sqlite(dict_list, 'testSite', 'LT5', db_name, 'unittesting')
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM unittesting")
        rows = cur.fetchall()
        self.assertEqual(len(rows), 3)
