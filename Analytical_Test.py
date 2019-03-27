from test_entity import test_entity
import pandas as pd
import numpy as np


def test_first_guess():

    AI = test_entity(5, 4)
    pool = AI.pool
    k = np.zeros((625, 625))
    df = pd.DataFrame( k , columns=pool, index= pool)

    df.to_csv(path_or_buf="tests_result.csv")
    for i in range(625):
        for j in range(625):
            AI.pool = pool
            df[pool[i]][pool[j]] = AI.get_reduction(pool[i],pool[j])
            print(i, j)

    df.to_csv(path_or_buf="tests_result.csv")

def test_second_guess():

    AI = test_entity(5, 4)
    original_pool = AI.pool

    reduced_pools = [] #Store the reduced pools of each code using first guess (1,1,2,3)

    #Filling reduced pools using 1,1,2,3 guess
    for i in range(len(original_pool)):
        code = original_pool[i]
        reduction = AI.get_reduction(code,AI.get_first_guess())
        print("Storing reduced pool for " + str(code) + "with reduction "  + str(reduction))
        reduced_pools.append(AI.pool)
        AI.pool = original_pool


    k = np.zeros((625, 625))
    df = pd.DataFrame( k , columns=original_pool, index= original_pool)
    df.to_csv(path_or_buf="tests_result2.csv")

    #Testing second guess
    #Now for each reduced pool we want to measure the reduction for every guess
    for i in range(625):
        for j in range(625):
            AI.pool = reduced_pools[i]
            df[original_pool[i]][original_pool[j]] = AI.get_reduction(original_pool[i],original_pool[j])
            print(i,j)

    df.to_csv(path_or_buf="tests_result2.csv")

if __name__== "__main__":
    #test_first_guess()
    test_second_guess()
