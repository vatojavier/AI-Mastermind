#AI entity that tests which guess is better

import itertools
import copy
import numpy as np
from random import randint


class test_entity:
    allColors = 0
    nPegs = 0
    pool = None     #Pool with all possible combinations, we don't know yet how big
    new_guess = None    #A new guess, we don't now yet how many pegs
    info = None     #Info given by comparing code with guess
    reduced_pool = []

    def __init__(self, allColors, nPegs):
        self.allColors = allColors
        self.nPegs = nPegs
        self.pool = self.generate_pool() #generate the pool depending on number of colors

    #Generates initial pool of 625 (with 5 different colors)
    def generate_pool(self):
        colors = []

        #creates the different colors [1,2,3,4,5] or more depending on allColors
        for i in range(self.allColors):
            colors.append(i + 1)

        #Inserting all possible permutations of colors in th pool
        pool = [p for p in itertools.product(colors, repeat=self.nPegs)]
        return pool

    #Makes a new guess to be compared with the code
    def guess(self):

        guess = self.pool[randint(0,len(self.pool) - 1)] #taking a random permutation from the pool
        self.new_guess = guess
        return guess

    #Returns the "black and white" info by comparing guess and code params
    def gen_info(self, guess, code):
        info = []
        black = 0
        white = 0

        #Converting guess and code to arrays to operate with them
        guess = np.array(guess)
        code = np.array(code)

        #Creating empy info     REMOVES HARDCODE BUT SLOW, MAYBE ENTER PARMETER AS ARRAY INSTEAD
        for i in range(self.nPegs):
            info.append(None)

        #info = np.array(info)

        peg_compare = copy.deepcopy(guess)
        code_compare = copy.deepcopy(code)

        for i in range(self.nPegs):
            if peg_compare[i] == code_compare[i]:
                black += 1
                peg_compare[i] = 0
                code_compare[i] = -1

        for i in range(self.nPegs):
            for j in range(self.nPegs):
                if (code_compare[i] == peg_compare[j]) and (i != j):
                    white += 1
                    peg_compare[j] = 0
                    code_compare[i] = -1
                    break

        for i in range(black):
            info[i] = 1

        for i in range(black, black + white):
            info[i] = 0

        return info

    #Reduces the pool and returns the reduction for the code and guess
    def get_reduction(self, code, guess):
        new_pool = []
        counter = 0
        self.new_guess = guess
        self.info = self.gen_info(code, guess)


        for combination in self.pool:
            new_info = self.gen_info(combination, self.new_guess)
            new_info = np.array(new_info)
            if np.array_equal(new_info, self.info):
                new_pool.append(combination)

        original_size = len(self.pool)
        new_size = len(new_pool)
        self.pool = new_pool

        return original_size - new_size
