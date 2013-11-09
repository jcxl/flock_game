import random
import bird

def random_position(config):
    max_size = config["size"]
    return ((random.randint(0, max_size[0]),
        random.randint(0, max_size[1])))

def populate(l, config):
    for x in range(config["num_birds"]):
        b = bird.Bird(random_position(config), (0, 0), x)
        l.append(b)

def multiply_vector(vector, scalar):
    l = [scalar * x for x in vector]
    return tuple(l)