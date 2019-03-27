from masterMind import gen_info
import itertools
import copy
import numpy as np
from random import randint


class AIEntity:
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

    def random_guess(self):
        guess = self.pool[randint(0,len(self.pool) - 1)] #taking a random permutation from the pool
        self.new_guess = guess
        return guess

    #Makes a new guess to be compared with the code
    def smart_guess(self):

        if len(self.pool) == 625: #If it's the first guees play smart guess
            print("Smart guess played")
            guess = self.first_guess()
            self.new_guess = guess
            return guess
        else:
            guess = self.pool[randint(0,len(self.pool) - 1)] #taking a random permutation from the pool
            self.new_guess = guess
            return guess

    #First guess that will reduce the maximum the pool
    def first_guess(self):
        smart_guess = [1,1,2,3]
        return smart_guess

    #Reduces the pool by selecting those combination that gives the same info
    def reduce_pool(self):
        new_pool = []
        counter = 0

        for combination in self.pool:
            new_info = gen_info(combination, self.new_guess)
            new_info = np.array(new_info)
            if np.array_equal(new_info, self.info):
                new_pool.append(combination)


        self.pool = new_pool
