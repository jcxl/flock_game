import pygame
import math

class Bird():

    def __init__(self, position, velocity, bird_id):
        self.MAX_ACCELERATION = 1
        self.MAX_TURN_RATE = 1
        self.MAX_SPEED = 1

        self.PERCEPTION_LIMIT = 1
        self.TOO_CLOSE = 1
        self.VISION_ANGLE = 160

        self.position = position
        self.velocity = velocity
        self.bird_id = bird_id

        
    def __str__(self):
        return "id: {} pos: ({}, {})".format(self.bird_id, self.position[0], self.position[1])

    def __repr__(self):
        return "id: {} pos: ({}, {})".format(self.bird_id, self.position[0], self.position[1])

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

    def birds_in_range(self, bird_list, perception_limit):
        pl_squared = perception_limit**2
        in_range = []

        for b in bird_list:
            if (self.bird_id == b.bird_id):
                continue

            distance_sqrd = self.distance_squared(b.position, self.position)
            if distance_sqrd < pl_squared:
                in_range.append(b)

        return in_range

    def heading(self):
        return math.atan2(self.velocity[1], self.velocity[0])

    def birds_in_angle(self, bird_list):
        in_angle = []
        
        for b in bird_list:
            x = self.diff_pos_x(b)
            y = self.diff_pos_y(b)
            b_angle = math.atan2(y, x)
            theta = math.fabs(b_angle - self.heading())
            if theta > math.pi:
                theta -= math.pi
            if theta < math.radians(self.VISION_ANGLE):
                in_angle.append(b)
            
        return in_angle

    def birds_in_view(self, bird_list):
        birds_in_range = self.birds_in_range(bird_list, self.PERCEPTION_LIMIT)
        birds_in_view = self.birds_in_angle(birds_in_range)

        return birds_in_view

    def cohesion_sensor(self, birds_in_view):
        x_comp = 0
        y_comp = 0

        for b in birds_in_view:
            x_comp += self.diff_pos_x(b)
            y_comp += self.diff_pos_y(b)

        x_comp = (x_comp * 1.0) / len(birds_in_view)
        y_comp = (y_comp * 1.0) / len(birds_in_view)

        return (x_comp, y_comp)

    def velocity_sensor(self, birds_in_view):
        x_comp = 0
        y_comp = 0

        for b in birds_in_view:
            x_comp += b.velocity[0]
            y_comp += b.velocity[1]

        x_comp = (x_comp * 1.0) / len(birds_in_view)
        y_comp = (y_comp * 1.0) / len(birds_in_view)

        return (x_comp, y_comp)

    def separation_sensor(self, birds_in_range):
        x_comp = 0
        y_comp = 0

        for b in birds_in_range:
            dist = math.sqrt(self.distance_squared(self.position, b.position))
            ratio = self.TOO_CLOSE / dist

            diff_pos_x = b.position[0] - self.position[0]
            diff_pos_y = b.position[1] - self.poisiton[1]

            unit_vector = (diff_pos_x / dist, diff_pos_y / dist)

            x_comp += (ratio - 1) * unit_vector[0]
            y_comp += (ratio - 1) * unit_vector[1]

        x_comp = x_comp / len(birds_in_range)
        y_comp = y_comp / len(birds_in_range)

        return (x_comp, y_comp)
