import pygame
import math
import util

class Predator():

    def __init__(self, position, velocity, prey_id, config = None):
        self.MAX_ACCELERATION = 1
        self.MAX_TURN_RATE = 1
        self.MAX_SPEED = 4        
        self.PREY_POS_WEIGHT = 100
        self.PREY_VEL_WEIGHT = 1.0
    
        self.position = position
        self.velocity = velocity
        self.prey_id = prey_id

        if config == None:
            config = {"size" : (800, 600)}
        
        self.config = config
    def get_rect(self):
        return pygame.Rect(self.position[0],self.position[1],8,8)

    def distance_squared(self, b):
        return self.diff_pos_x(b)**2 + self.diff_pos_y(b)**2

    def diff_pos_x(self, b):
        return b.position[0] - self.position[0]

    def diff_pos_y(self, b):
        return b.position[1] - self.position[1]

    def detect_closest_prey(self, prey_list):
        shortest_dist = 200000000
        prey = None

        for p in prey_list:
            new_dist = self.distance_squared(p)
            if new_dist < shortest_dist:
                prey = p
                shortest_dist = new_dist
        
        return prey

    def get_closest_prey_position(self, prey_list):
        closest_prey = self.detect_closest_prey(prey_list)

        rel_pos = [0, 0]

        rel_pos[0] = self.position[0] - closest_prey.position[0]
        rel_pos[1] = self.position[1] - closest_prey.position[1]

        return rel_pos

    def get_closest_prey_velocity(self, prey_list):
        return self.detect_closest_prey(prey_list).velocity
    
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

        prey_pos_vector = self.get_closest_prey_position(prey_list)
        vectors.append(util.multiply_vector(prey_pos_vector, self.PREY_POS_WEIGHT))

        prey_vel_vector = self.get_closest_prey_velocity(prey_list)
        vectors.append(util.multiply_vector(prey_vel_vector, self.PREY_VEL_WEIGHT))

        vectors.append(util.multiply_vector(self.edge_repulsion_sensor(), 100))

        print vectors

        print """Prey_Pos: {}
        Prey_Vel: {}
        Repulsion: {}""".format(*vectors)

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
        self.velocity = vector_sum

        new_pos = (self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1])
        self.position = new_pos
