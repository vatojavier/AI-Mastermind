from AIEntity import AIEntity
import pandas as pd
import numpy as np

AI = AIEntity(5, 4)
pool = AI.pool
k = np.zeros((625, 625))
df = pd.DataFrame( k , columns=pool, index= pool)
df.to_csv(path_or_buf="Address")
