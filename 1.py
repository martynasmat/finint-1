import pandas as pd
import numpy as np
import datetime

dates = pd.date_range('20190214', periods=6)
numbers = np.matrix([[ 101, 103], [105.5, 75], [102, 80.3], [100, 85], [110, 98], [109.6, 125.7 ]] )
df = pd.DataFrame(numbers, index=dates, columns=['A','B'])

def fetch_by_index(idx: str):
    return df.loc[idx]

print(fetch_by_index('20190218'))
