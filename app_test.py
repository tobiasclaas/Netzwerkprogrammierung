import unittest
from app import *


# to run
# python -m unittest test_app
class TestApp(unittest.TestCase):

    def test_does_master_exist(self):
        self.assertEqual(does_master_exist({
            'http://127.0.0.1:5000': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5001': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5002': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5003': (True, 'http://127.0.0.1:5003'),
            'http://127.0.0.1:5004': (False, None)
            }), 'http://127.0.0.1:5000')
        self.assertEqual(does_master_exist({
            'http://127.0.0.1:5000': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5001': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5002': (True, 'http://127.0.0.1:5003'),
            'http://127.0.0.1:5003': (True, 'http://127.0.0.1:5003'),
            'http://127.0.0.1:5004': (False, None)
            }), None)
        self.assertEqual(does_master_exist({
            'http://127.0.0.1:5000': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5001': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5002': (False, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5003': (False, 'http://127.0.0.1:5003'),
            'http://127.0.0.1:5004': (False, None)
            }), None)
        self.assertEqual(does_master_exist({
            'http://127.0.0.1:5000': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5001': (True, 'http://127.0.0.1:5000'),
            'http://127.0.0.1:5002': (True, None),
            'http://127.0.0.1:5003': (True, None),
            'http://127.0.0.1:5004': (False, None)
            }), None)

    def test_determine_new_master(self):
        self.assertEqual(determine_new_master({
            'http://127.0.0.1:5000': (False, None),
            'http://127.0.0.1:5001': (True, None),
            'http://127.0.0.1:5002': (True, None),
            'http://127.0.0.1:5003': (True, None),
            'http://127.0.0.1:5004': (False, None)
            }), 'http://127.0.0.1:5001')
        self.assertEqual(determine_new_master({
            'http://127.0.0.1:5000': (True, None),
            'http://127.0.0.1:5001': (True, None),
            'http://127.0.0.1:5002': (False, None),
            'http://127.0.0.1:5003': (False, None),
            'http://127.0.0.1:5004': (True, None)
        }), 'http://127.0.0.1:5000')
