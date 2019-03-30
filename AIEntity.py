from masterMind import gen_info
import itertools
import numpy as np
from random import randint


class AIEntity:
    allColors = 0
    nPegs = 0
    pool = None  # Pool with all possible combinations, we don't know yet how big
    new_guess = None  # A new guess, we don't now yet how many pegs
    info = None  # Info given by comparing code with guess
    reduced_pool = []
    step = 0  # Number of guesses played

    def __init__(self, all_colors, n_pegs):
        self.allColors = all_colors
        self.nPegs = n_pegs
        self.pool = self.generate_pool()  # generate the pool depending on number of colors

    # Generates initial pool of 625 (with 5 different colors and 4 pegs)
    def generate_pool(self):
        colors = []

        # creates the different colors [1,2,3,4,5] or more depending on allColors
        for i in range(self.allColors):
            colors.append(i + 1)

        # Inserting all possible permutations of colors in th pool
        pool = [p for p in itertools.product(colors, repeat=self.nPegs)]
        return pool

    # Generates an actual guess depending in the step and computing the heuristic search
    def generate_guess(self):

        if self.step == 0:  # If it's the first guess...
            self.step += 1
            self.new_guess = self.first_guess()
            return self.new_guess
        else:   # Otherwise search the tree to generate heuristics
            h = np.zeros(len(self.pool))
            j = 0
            min_h = len(self.pool)

            for guess in self.pool:
                h[j] = self.heuristic(guess, 0, min_h)

                if h[j] < min_h:
                    min_h = h[j]
                j = +1

            h_min_index = np.argmin(h)
            best_guess = self.pool[h_min_index]
            self.new_guess = best_guess

        self.step += 1
        return self.new_guess

    def random_guess(self):
        guess = self.pool[randint(0, len(self.pool) - 1)]  # taking a random permutation from the pool
        self.new_guess = guess
        return guess

    # First guess that will reduce the maximum the pool
    @staticmethod
    def first_guess():

        smart_guess = [1, 2]
        return smart_guess

    # Reduces the pool by selecting those combination that gives the same info
    def reduce_pool(self):
        new_pool = []

        for combination in self.pool:
            new_info = gen_info(combination, self.new_guess)
            new_info = np.array(new_info)
            if np.array_equal(new_info, self.info):
                new_pool.append(combination)

        self.pool = new_pool

    def heuristic(self, guess, depth, min_h):

        if len(self.pool) == 1:
            return 1

        # print("Depth: " + str(depth))
        if depth == 2:
            return len(self.pool)
        depth += 1
        info_set = set()
        self.new_guess = guess
        for combination in self.pool:
            info_set.add(tuple(gen_info(guess, combination)))

        entity_array = self.create_array(len(info_set))

        i = 0
        pools_sum = 0
        for info in info_set:
            entity_array[i].info = list(info)
            entity_array[i].reduce_pool()
            pools_sum += len(entity_array[i].pool)
            i += 1

        avg_poolsize = pools_sum / i

        i = 0
        max_pool = []
        for info in info_set:
            if len(entity_array[i].pool) >= avg_poolsize:
                H = []  # Array of length = A[i].pool
                for guess in entity_array[i].pool:
                    H.append(entity_array[i].heuristic(guess, depth, min_h))
                max_heuristic = min(H)

                if max_heuristic > min_h:
                    return max_heuristic
                max_pool.append(max_heuristic)
            i += 1

        return max(max_pool)

    # Return array of AI objects
    def create_array(self, length):
        array = []
        for i in range(length):
            AI = AIEntity(self.allColors, self.nPegs)
            AI.pool = self.pool
            AI.new_guess = self.new_guess
            array.append(AI)
        return array
