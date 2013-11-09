import unittest
from .. import util

class TestMainFunctions(unittest.TestCase):

    def test_random_position(self):
        config = {"size": (100, 200)}
        pos = util.random_position(config)
        self.assertTrue(0 <= pos[0] <= config["size"][0])
        self.assertTrue(0 <= pos[1] <= config["size"][1])