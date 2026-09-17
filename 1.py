import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

dates = pd.date_range('20190214', periods=6)
numbers = np.matrix([[ 101, 103], [105.5, 75], [102, 80.3], [100, 85], [110, 98], [109.6, 125.7 ]] )
frame = pd.DataFrame(numbers, index=dates, columns=['A','B'])


def fetch_by_index(df: pd.DataFrame, idx: str | datetime.datetime) -> pd.Series:
    return df.loc[idx]


def fetch_second_to_last(df: pd.DataFrame) -> pd.Series:
    return df.iloc[-2]


def fetch_first_two(df: pd.DataFrame) -> pd.Series:
    return df['B'].head(2)


def desc_b(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by='B', ascending=False)


def filter_a(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['A'] > 105]


def plot_a(df: pd.DataFrame) -> None:
    df.plot(y='A')
    plt.show()
    return


def remove_a_less_than_b(df: pd.DataFrame):
    df.drop(index=df.index[df['A'] < df['B']], inplace=True)
    return

print(fetch_by_index(frame, '20190218'))
print('\n')
print(fetch_by_index(frame, datetime.datetime(2019, 2, 18)))
print('\n')
print(fetch_second_to_last(frame))
print('\n')
print(fetch_first_two(frame))
print('\n')
print(desc_b(frame))
print('\n')
print(filter_a(frame))
print('\n')
print(plot_a(frame))
print('\n')
remove_a_less_than_b(frame)
print(frame)
print('\n')