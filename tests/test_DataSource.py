# tests/test_DataSource.py
import unittest
from DataSource import DataSource

class TestDataSource(unittest.TestCase):

    def setUp(self):
        self.data_source = DataSource()

    def test_get_light_pollution(self):
        coordinate = (33.53210, -5.10950)
        result = self.data_source.get_light_pollution(coordinate)
        self.assertIsNotNone(result)

    

if __name__ == '__main__':
    unittest.main()
