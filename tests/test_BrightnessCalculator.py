import unittest
from Processing.BrightnessCalculator import BrightnessCalculator

class TestBrightnessCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = BrightnessCalculator("sample_data")

    def test_compute_brightness_data(self):
        result = self.calculator.compute_brightness_data()
        self.assertIsNotNone(result)

    

if __name__ == '__main__':
    unittest.main()
#python -m unittest discover tests