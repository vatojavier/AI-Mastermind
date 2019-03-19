import itertools
import copy
import numpy as np


class AIEntity:
        guess = np.zeros((4,), dtype=int)
        info = np.zeros((4,), dtype=int)
        pool = np.zeros((625,), dtype=int)#[4,256] array
        size = 0
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
            return pool

        #makes a new guess
        def guess(self):

            guess = np.random.randint(1,high=self.allColors + 1, size=self.nPegs)
            return guess

        def gen_info(self,guess, code):
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
            new_pool = np.zeros((625,),dtype=int)
            counter = 0
            for i in range(0,self.size):
                new_info = self.gen_info(self.pool[i], self.guess)
                if new_info == self.info:
                    counter += 1
                    new_pool[counter] = i

            self.pool = new_pool
            self.size = counter

