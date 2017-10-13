import numpy as np
import pandas as pd
data = np.array([['Time','Monday','TUESDAY'],
                ['00:00',"Monday",2],
                ['01:00',"Tuesday",4]])

print(pd.DataFrame(data=data[1:,1:],
                  index=data[1:,0],
                  columns=data[0,1:]))
