import random
import prey
import math

def random_position(config):
    max_size = config["size"]
    return ((random.randint(0, max_size[0]),
        random.randint(0, max_size[1])))

def populate_prey(l, config):
    for x in range(config["num_birds"]):
        b = prey.Prey(random_position(config), (random.randint(0, 5), random.randint(0, 5)), x, config)
        l.append(b)

def populate_predators(l, config):
    for x in range(config["num_predators"]):
        b = predator.Predator(random_position(config), (random.randint(0, 5), random.randint(0, 5)), x, config)
        l.append(b)


def multiply_vector(vector, scalar):
    l = [scalar * x for x in vector]
    return tuple(l)

def vector_magnitude(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)
