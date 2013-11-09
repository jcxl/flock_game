import unittest
from .. import prey

class TestPrey(unittest.TestCase):

    def test_in_range(self):
        b1 = prey.Prey((0, 0), (0, 0), 0)
        b2 = prey.Prey((5, 5), (0, 0), 1)
        b3 = prey.Prey((10, 10), (0, 0), 2)

        b_list = [b1, b2, b3]
        in_range = b1.entities_in_range(b_list, 8)
        self.assertEquals(in_range[0].prey_id, 1)
        self.assertEquals(len(in_range), 1)

    def test_in_angle(self):
        b1 = prey.Prey((0, 0), (0, 1), 0)
        b2 = prey.Prey((0, -5), (0, 0), 1)
        b3 = prey.Prey((-2, -2), (0, 0), 2)
        
        b_list = [b2, b3]
        in_angle = b1.entities_in_angle(b_list)
        self.assertEquals(in_angle[0].prey_id, 2)
        self.assertEquals(len(in_angle), 1)

    def test_in_angle_2(self):
        b1 = prey.Prey((0, 0), (-1, -1), 0)
        b2 = prey.Prey((5, 5), (0, 0), 1)
        b3 = prey.Prey((-2, -2), (0, 0), 2)
    
        b_list = [b2, b3]
        in_angle = b1.entities_in_angle(b_list)
        self.assertEquals(in_angle[0].prey_id, 2)
        self.assertEquals(len(in_angle), 1)

    def test_in_angle_3(self):
        b1 = prey.Prey((0, 0), (-1, 0), 0)
        b2 = prey.Prey((5, 0), (0, 0), 1)
        b3 = prey.Prey((0, 0), (0, 0), 2)
    
        b_list = [b2, b3]
        in_angle = b1.entities_in_angle(b_list)
        self.assertEquals(in_angle[0].prey_id, 2)
        self.assertEquals(len(in_angle), 1)

    def test_cohesion(self):

        b1 = prey.Prey((0, 0), (0, 1), 0)
        b2 = prey.Prey((2, 1), (0, 2), 1)
        b3 = prey.Prey((-1, 1), (0, 2), 2)

        b_list = [b1, b2, b3]

        vector = b1.cohesion_vector(b_list)
        self.assertEquals((0.5, 1.0), vector)

    def test_velocity(self):

        b1 = prey.Prey((0, 0), (0, 1), 0)
        b2 = prey.Prey((1, 1), (1, 2), 1)
        b3 = prey.Prey((-1, 1), (-1, 2), 2)

        b_list = [b1, b2, b3]

        vector = b1.follow_vector(b_list)        
        self.assertEquals((0.0, 2.0), (0.0, 2.0))

    def test_separation(self):

        b1 = prey.Prey((0, 0), (0, 1), 0)
        b2 = prey.Prey((1, 1), (1, 2), 1)
        b3 = prey.Prey((-1, 1), (-1, 2), 2)

        b_list = [b1, b2, b3]

        vector = b1.separation_vector(b_list)
        self.assertEquals((0.0, -4.292893218813452), vector)
