import unittest
from ScoreCache import ScoreCache

class TestScoreCache(unittest.TestCase):

    def setUp(self):
        self.cache = ScoreCache([(33.53210, -5.10950)])

    def test_get_best_coordinate(self):
        coord, score = self.cache.get_best_coordinate()
        self.assertIsNotNone(coord)
        self.assertIsNotNone(score)

    

if __name__ == '__main__':
    unittest.main()
