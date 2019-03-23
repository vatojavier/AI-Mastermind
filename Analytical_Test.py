from test_entity import test_entity
import pandas as pd
import numpy as np

AI = test_entity(5, 4)
pool = AI.pool
k = np.zeros((625, 625))
df = pd.DataFrame( k , columns=pool, index= pool)
df.to_csv(path_or_buf="tests_result.csv")

df[(1,1,1,1)][(1,1,1,1)] = 5



for i in range(10):
    for j in range(10):
        AI = test_entity(5, 4)
        df[pool[i]][pool[j]] = AI.get_reduction(pool[i],pool[j])


df.to_csv(path_or_buf="tests_result.csv")
