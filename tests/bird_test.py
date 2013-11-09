import unittest
from .. import bird

class TestBird(unittest.TestCase):

    def test_in_range(self):
        b1 = bird.Bird((0, 0), (0, 0), 0)
        b2 = bird.Bird((5, 5), (0, 0), 1)
        b3 = bird.Bird((10, 10), (0, 0), 2)

        b_list = [b1, b2, b3]
        in_range = b1.birds_in_range(b_list, 8)
        self.assertEquals(in_range[0].bird_id, 1)
        self.assertEquals(len(in_range), 1)