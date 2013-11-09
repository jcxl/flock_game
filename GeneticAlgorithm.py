import math
import random

    MUTATION_CHANCE = 0.5
    def select_parent(survivor_hash):
        selection_list = []
        key_list = survivor_hash.keys()
        
        for x in key_list:
            i = 0
            while survivor_hash[x] > i:
                selection_list.append(survivor_hash[x])
                i += 1
        
        index = random.randint(0, len(selection_list))
        return selection_list(index)

    def mutate_parent(parent_weights):
        new_weights = []

        for w in parent_weights:
            if random.random() > MUTATION_CHANCE:
                w = random.gauss(w,w * .1)
                new_weights.append(w)
            else:
                new_weights.append(w)

        return new_weights.reverse()

            
