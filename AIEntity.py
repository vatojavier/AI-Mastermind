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


    def heuristic(self, guess, depth, min_h):

        if len(self.pool) == 1:
            return 1

        #print("Depth: " + str(depth))
        if depth == 2:
            return len(self.pool)
        depth += 1
        info_set = set()
        self.new_guess = guess
        for combination in self.pool:

            info_set.add(tuple(gen_info(guess,combination)))

        A = self.create_array(len(info_set))

        i = 0
        pools_sum = 0
        for info in info_set:
            A[i].info = list(info)
            A[i].reduce_pool()
            pools_sum += len(A[i].pool)
            i += 1

        avg_poolsize = pools_sum / i

        i = 0
        max_pool = []
        for info in info_set:
            #print("info: "+ str(info))
            #print("Lengt " + str(len(A[i].pool)))
            #print(avg_poolsize)
            if len(A[i].pool) >= avg_poolsize:
                #print("Expanding pool of " + str(i))
                H = [] #Array of length = A[i].pool
                for guess in A[i].pool:
                    #print(guess)
                    H.append(A[i].heuristic(guess, depth, min_h))
                max_heuristic = min(H)
                #print("Heuristic of " + str(info) + str(H))

                if (max_heuristic > min_h):
                        #print("Max heuristic too large")
                        return max_heuristic
                max_pool.append(max_heuristic)
            i += 1
        #print(max_pool)

        return max(max_pool)

    #Return array of AI objects
    def create_array(self,length):
        A = []
        for i in range(length):
            AI = AIEntity(self.allColors,self.nPegs)
            AI.pool = self.pool
            AI.new_guess = self.new_guess
            A.append(AI)
        return A
