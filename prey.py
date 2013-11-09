import pygame
import util
import math

class Prey():

    def __init__(self, position, velocity, prey_id, config=None):
        self.MAX_ACCELERATION = 1
        self.MAX_TURN_RATE = 1
        self.MAX_SPEED = 5

        self.PERCEPTION_LIMIT = 200
        self.TOO_CLOSE = 50
        self.VISION_ANGLE = 160

        self.COHESION_WEIGHT = 1.0
        self.FOLLOW_WEIGHT = 5
        self.SEPARATION_WEIGHT = 100
        self.PREDATOR_WEIGHT = 1.0

        self.position = position
        self.velocity = velocity
        self.prey_id = prey_id

        if config == None:
            config = {"size": (800, 600)}
        self.config = config
        
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

    def entities_in_range(self, prey_list, perception_limit):
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

    def entities_in_angle(self, prey_list):
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

    def entities_in_view(self, prey_list):
        entities_in_range = self.entities_in_range(prey_list, self.PERCEPTION_LIMIT)
        entities_in_view = self.entities_in_angle(entities_in_range)

        return entities_in_view

    def cohesion_vector(self, prey_list):
        entities_in_view = self.entities_in_view(prey_list)
        return self.cohesion_sensor(entities_in_view)

    def cohesion_sensor(self, entities_in_view):

        if len(entities_in_view) == 0:
            return (0.0, 0.0)

        x_comp = 0
        y_comp = 0

        for b in entities_in_view:
            x_comp += self.diff_pos_x(b)
            y_comp += self.diff_pos_y(b)

        x_comp = (x_comp * 1.0) / len(entities_in_view)
        y_comp = (y_comp * 1.0) / len(entities_in_view)

        return (x_comp, y_comp)

    def follow_vector(self, prey_list):
        entities_in_view = self.entities_in_view(prey_list)
        return self.velocity_sensor(entities_in_view)

    def velocity_sensor(self, entities_in_view):

        if len(entities_in_view) == 0:
            return (0.0, 0.0)

        x_comp = 0
        y_comp = 0

        for b in entities_in_view:
            x_comp += b.velocity[0]
            y_comp += b.velocity[1]

        x_comp = (x_comp * 1.0) / len(entities_in_view)
        y_comp = (y_comp * 1.0) / len(entities_in_view)

        return (x_comp, y_comp)

    def separation_vector(self, prey_list):
        prey_too_close = self.entities_in_range(prey_list, self.TOO_CLOSE)
        entities_in_view = self.entities_in_view(prey_too_close)
        return self.generic_repulsion_sensor(entities_in_view, self.TOO_CLOSE)

    def predator_vector(self, predator_list):
        predators_in_view = self.entities_in_view(predator_list)
        return self.generic_repulsion_sensor(predators_in_view, self.PERCEPTION_LIMIT)

    def generic_repulsion_sensor(self, entity_list, radius):

        if len(entity_list) == 0:
            return (0.0, 0.0)

        x_comp = 0
        y_comp = 0

        for e in entity_list:
            dist = math.sqrt(self.distance_squared(self.position, e.position))
            ratio = radius / dist

            diff_pos_x = self.position[0] - e.position[0]
            diff_pos_y = self.position[1] - e.position[1]

            unit_vector = (diff_pos_x / dist, diff_pos_y / dist)

            x_comp += (ratio - 1) * unit_vector[0]
            y_comp += (ratio - 1) * unit_vector[1]

        x_comp = x_comp / len(entity_list)
        y_comp = y_comp / len(entity_list)

        return (x_comp, y_comp)

    def edge_repulsion_sensor(self):
        x_comp = 0
        y_comp = 0

        if self.position[0] < 100:
            x_comp = ((100.0 / self.position[0]) - 1)
        elif self.position[0] + 100 > self.config['size'][0]:
            x_comp = ((100.0 / self.config['size'][0] - self.position[0]) - 1)

        if self.position[1] < 100:
            y_comp = ((100.0 / self.position[1]) - 1)
        elif self.position[1] + 100 > self.config['size'][1]:
            y_comp = ((100.0 / self.config['size'][1] - self.position[1]) - 1)

        return (x_comp, y_comp)

    def sum_sensors(self, prey_list, predator_list):
        vectors = []

        cohesion_vector = self.cohesion_vector(prey_list)
        vectors.append(util.multiply_vector(cohesion_vector, self.COHESION_WEIGHT))

        follow_vector = self.follow_vector(prey_list)
        vectors.append(util.multiply_vector(follow_vector, self.FOLLOW_WEIGHT))

        separation_vector = self.separation_vector(prey_list)
        vectors.append(util.multiply_vector(separation_vector, self.SEPARATION_WEIGHT))

        predator_vector = self.predator_vector(predator_list)
        vectors.append(util.multiply_vector(predator_vector, self.PREDATOR_WEIGHT))

        vectors.append(self.edge_repulsion_sensor())

        x_comp = 0
        y_comp = 0

        for x, y in vectors:
            x_comp += x
            y_comp += y

        vector_magnitude = util.vector_magnitude((x_comp, y_comp))

        if vector_magnitude > self.MAX_SPEED:
            x_comp /= vector_magnitude
            y_comp /= vector_magnitude

            x_comp *= self.MAX_SPEED
            y_comp *= self.MAX_SPEED

        return (x_comp, y_comp)

    def tick(self, prey_list, predator_list):
        vector_sum = self.sum_sensors(prey_list, predator_list)
        new_velocity = [0, 0]
        if vector_sum[0] > self.velocity[0] and vector_sum[0] - self.velocity[0] > self.MAX_ACCELERATION:
            new_velocity[0] = self.velocity[0] + self.MAX_ACCELERATION
        elif vector_sum[0] > self.velocity[0] and vector_sum[0] - self.velocity[0] < self.MAX_ACCELERATION:
            new_velocity[0] = self.velocity[0] + vector_sum[0] - self.velocity[0]
        elif vector_sum[0] < self.velocity[0] and self.velocity[0] - vector_sum[0] > self.MAX_ACCELERATION:
            new_velocity[0] = self.velocity[0] - self.MAX_ACCELERATION
        elif vector_sum[0] > self.velocity[0] and vector_sum[0] - self.velocity[0] < self.MAX_ACCELERATION:
            new_velocity[0] = self.velocity[0] - self.velociy[0] - vector_sum[0]

        if vector_sum[1] > self.velocity[1] and vector_sum[1] - self.velocity[1] > self.MAX_ACCELERATION:
            new_velocity[1] = self.velocity[1] + self.MAX_ACCELERATION
        elif vector_sum[1] > self.velocity[1] and vector_sum[1] - self.velocity[1] < self.MAX_ACCELERATION:
            new_velocity[1] = self.velocity[1] + vector_sum[1] - self.velocity[1]
        elif vector_sum[1] < self.velocity[1] and self.velocity[1] - vector_sum[1] > self.MAX_ACCELERATION:
            new_velocity[1] = self.velocity[1] - self.MAX_ACCELERATION
        elif vector_sum[1] > self.velocity[1] and vector_sum[1] - self.velocity[1] < self.MAX_ACCELERATION:
            new_velocity[1] = self.velocity[1] - self.velociy[1] - vector_sum[1]


        self.velocity= new_velocity
        new_pos = (self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1])
        self.position = new_pos


        
