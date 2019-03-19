import itertools
import copy
import numpy as np
from random import randint


class AIEntity:
        guess = np.zeros((4,), dtype=int)
        info = np.zeros((4,), dtype=int)
        pool = np.zeros((625,), dtype=int)#[4,256] array
        size = 0    #size of the new reduced pool
        allColors = 0
        nPegs = 0

        def __init__(self, allColors, nPegs):
            self.allColors = allColors
            self.nPegs = nPegs
            self.pool = self.generate_pool() #generate the pool depending on number of colors

        #generates initial pool of 625 (with 5 different colors)
        def generate_pool(self):
            colors = []

            for i in range(self.allColors):
                colors.append(i + 1)

            pool_list = [p for p in itertools.product(colors, repeat=4)]
            pool = np.array(pool_list)
            self.size = len(pool)
            return pool

        #makes a new guess
        def guess(self):

            guess = self.pool[randint(0,self.size)] #taking a random permutation from the pool
            self.guess = guess
            return guess

        #return a "black and white" info by comparing guess and code params as arrays
        def gen_info(self, guess, code):
            info = [None, None, None, None]
            black = 0
            white = 0
            peg_compare = copy.deepcopy(guess)
            code_compare = copy.deepcopy(code)

            for i in range(4):
                if peg_compare[i] == code_compare[i]:
                    black += 1
                    peg_compare[i] = 0
                    code_compare[i] = -1

            for i in range(4):
                for j in range(4):
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

        # reduces the pool
        def reduce_pool(self):
            new_pool = [] #np.zeros((625,),dtype=int)
            counter = 0

            for i in range(0,self.size):
                #print(self.guess)

                new_info = self.gen_info(self.pool[i], self.guess)
                new_info = np.array(new_info)
                if np.array_equal(new_info, self.info):
                    new_pool.append(self.pool[i])



            self.pool = new_pool
            self.size = counter
