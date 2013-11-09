import pygame


class Bird():

    def __init__(self, position, velocity, bird_id):
        self.MAX_ACCELERATION = 1
        self.MAX_TURN_RATE = 1
        self.MAX_SPEED = 1

        self.PERCEPTION_LIMIT = 1
        self.TOO_CLOSE = 1
        self.VISION_ANGLE = 1

        self.position = position
        self.velocity = velocity
        self.bird_id = bird_id

    def __str__(self):
        return str(self.bird_id)

    def __repr__(self):
        return str(self.bird_id)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1],
            5, 5)

    def distance_squared(self, pos1, pos2):
        x_comp = (pos1[0] - pos2[0])
        y_comp = (pos1[1] - pos2[1])

        return (x_comp**2 + y_comp**2)

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