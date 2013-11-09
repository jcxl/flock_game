import pygame
import math

class Prey():

    def __init__(self, position, velocity, prey_id):
        self.MAX_ACCELERATION = 1
        self.MAX_TURN_RATE = 1
        self.MAX_SPEED = 1

        self.PERCEPTION_LIMIT = 100
        self.TOO_CLOSE = 10
        self.VISION_ANGLE = 160

        self.position = position
        self.velocity = velocity
        self.prey_id = prey_id

        
    def __str__(self):
        return "id: {} pos: ({}, {})".format(self.prey_id, self.position[0], self.position[1])

    def __repr__(self):
        return "id: {} pos: ({}, {})".format(self.prey_id, self.position[0], self.position[1])

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1],
            5, 5)

    def distance_squared(self, pos1, pos2):
        x_comp = (pos1[0] - pos2[0])
        y_comp = (pos1[1] - pos2[1])

        return (x_comp**2 + y_comp**2)
    
    def diff_pos_x(self, b):
        return b.position[0] - self.position[0]

    def diff_pos_y(self, b):
        return b.position[1] - self.position[1]

    def prey_in_range(self, prey_list, perception_limit):
        pl_squared = perception_limit**2
        in_range = []

        for b in prey_list:
            if (self.prey_id == b.prey_id):
                continue

            distance_sqrd = self.distance_squared(b.position, self.position)
            if distance_sqrd < pl_squared:
                in_range.append(b)

        return in_range

    def heading(self):
        return math.atan2(self.velocity[1], self.velocity[0])

    def prey_in_angle(self, prey_list):
        in_angle = []
        
        for b in prey_list:
            x = self.diff_pos_x(b)
            y = self.diff_pos_y(b)

            if (x == 0 and y == 0):
                in_angle.append(b)
                continue

            b_angle = math.atan2(y, x)
            theta = math.fabs(b_angle - self.heading())
            if theta > math.pi:
                theta -= math.pi
            if theta < math.radians(self.VISION_ANGLE):
                in_angle.append(b)
            
        return in_angle

    def prey_in_view(self, prey_list):
        prey_in_range = self.prey_in_range(prey_list, self.PERCEPTION_LIMIT)
        prey_in_view = self.prey_in_angle(prey_in_range)

        return prey_in_view

    def cohesion_vector(self, prey_list):
        prey_in_view = self.prey_in_view(prey_list)
        return self.cohesion_sensor(prey_in_view)

    def cohesion_sensor(self, prey_in_view):
        x_comp = 0
        y_comp = 0

        for b in prey_in_view:
            x_comp += self.diff_pos_x(b)
            y_comp += self.diff_pos_y(b)

        x_comp = (x_comp * 1.0) / len(prey_in_view)
        y_comp = (y_comp * 1.0) / len(prey_in_view)

        return (x_comp, y_comp)

    def follow_vector(self, prey_list):
        prey_in_view = self.prey_in_view(prey_list)
        return self.velocity_sensor(prey_in_view)

    def velocity_sensor(self, prey_in_view):
        x_comp = 0
        y_comp = 0

        for b in prey_in_view:
            x_comp += b.velocity[0]
            y_comp += b.velocity[1]

        x_comp = (x_comp * 1.0) / len(prey_in_view)
        y_comp = (y_comp * 1.0) / len(prey_in_view)

        return (x_comp, y_comp)

    def separation_vector(self, prey_list):
        prey_too_close = self.prey_in_range(prey_list, self.TOO_CLOSE)
        prey_in_view = self.prey_in_view(prey_too_close)
        return self.separation_sensor(prey_in_view)

    def separation_sensor(self, prey_in_range):
        x_comp = 0
        y_comp = 0

        for b in prey_in_range:
            dist = math.sqrt(self.distance_squared(self.position, b.position))
            ratio = self.TOO_CLOSE / dist

            diff_pos_x = self.position[0] - b.position[0]
            diff_pos_y = self.position[1] - b.position[1]

            unit_vector = (diff_pos_x / dist, diff_pos_y / dist)

            x_comp += (ratio - 1) * unit_vector[0]
            y_comp += (ratio - 1) * unit_vector[1]

        x_comp = x_comp / len(prey_in_range)
        y_comp = y_comp / len(prey_in_range)

        return (x_comp, y_comp)