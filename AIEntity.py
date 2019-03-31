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

    def random_guess(self):
        guess = self.pool[randint(0, len(self.pool) - 1)]  # taking a random permutation from the pool
        self.new_guess = guess
        return guess

    # First guess that will reduce the maximum the pool
    @staticmethod
    def first_guess():

        smart_guess = [1, 1, 2, 3]
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

    # Generates an actual guess choosing the MINIMUM heuristic
    def generate_guess(self):

        if self.step == 0:  # If it's the first guess...
            self.new_guess = self.first_guess()

        else:  # Otherwise search the tree to generate heuristics
            h = np.zeros(len(self.pool), dtype=int)
            j = 0
            min_h = len(self.pool)

            for guess in self.pool:
                #print("loop")
                h[j] = self.heuristic(guess, 0, min_h)
                #print("Heuristic of guess" + str(guess) + " is " + str(h[j]))

                if h[j] < min_h:
                    min_h = h[j]
                j += 1

            h_min_index = np.argmin(h)
            #print("The min index is: " + str(h_min_index))
            best_guess = self.pool[h_min_index]
            self.new_guess = best_guess
            #print(str(h))
            #print("So the new guess is: " + str(self.new_guess))
        self.step += 1
        return self.new_guess

    # Generates heuristic by returning the MAXIMUM pool size of the pools at selected depth
    def heuristic(self, guess, depth, min_h):
        #self.c_print("For guess " + str(guess) + ": ", depth)
        #self.c_print("Depth: " + str(depth),depth)
        print("In depth " + str(depth))
        if len(self.pool) == 1:
            #self.c_print("Min pool size of 1 reached", depth)
            return 1

        # print("Depth: " + str(depth))
        if depth == 3:
            #self.c_print("Max depth reached, returning pool size of " + str(len(self.pool)), depth)
            return len(self.pool)

        depth += 1
        info_set = set()
        self.new_guess = guess
        for combination in self.pool:  # Generating all infos for every combination in the pool:
            info_set.add(tuple(gen_info(guess, combination)))

        entity_array = self.create_array(len(info_set))

        i = 0
        pools_sum = 0
        #self.c_print("Possible infos: ", depth)
        for info in info_set:
            entity_array[i].info = list(info)
            entity_array[i].reduce_pool()
            #self.c_print(str(info) + " with pool size of " + str(len(entity_array[i].pool)), depth)
            pools_sum += len(entity_array[i].pool)
            i += 1

        avg_poolsize = pools_sum / i
        #self.c_print("Average pool size of depth " + str(depth) + ": " + str(avg_poolsize), depth)

        max_pool = []
        for i in range(len(info_set)):
            #self.c_print("Pool of this info: " + str(entity_array[i].pool), depth)
            if len(entity_array[i].pool) >= avg_poolsize:
                heuristic = []  # Array of length = A[i].pool
                for guess in entity_array[i].pool:
                    heuristic.append(entity_array[i].heuristic(guess, depth, min_h))
                min_heuristic = min(heuristic)

                if min_heuristic > min_h:
                    return min_heuristic
                max_pool.append(min_heuristic)  # Adding to max_pool the minimum heuristic

        #self.c_print("Returning " + str(max(max_pool)), depth)
        return max(max_pool)  # Returning the maximum of the minimum heuristic haha

    # Return array of AI objects
    def create_array(self, length):
        array = []
        for i in range(length):
            AI = AIEntity(self.allColors, self.nPegs)
            AI.pool = self.pool
            AI.new_guess = self.new_guess
            array.append(AI)
        return array

    def c_print(self, arg, depth):

        for i in range(depth):
            print("\t", end=" ")

        print(arg)

