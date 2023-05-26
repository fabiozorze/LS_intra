import pandas as pd
import yfinance
import numpy as np


def aZ_score(df, lookback, long, short):

    meanSpread = df.spread.rolling(window=lookback).mean()
    stdSpread = df.spread.rolling(window=lookback).std()
    df['zScore'] = (df.spread - meanSpread) / stdSpread

    df['short'] = short
    df['long'] = long

    # Long positions
    df['long_entry'] = df['zScore'] < long
    df['long_exit'] = df['zScore'] > 0

    df['positions_long'] = np.nan
    df.loc[df.long_entry, 'positions_long'] = 1
    df.loc[df.long_exit, 'positions_long'] = 0
    df.positions_long = df.positions_long.fillna(method='ffill')

    # Short positions
    df['short_entry'] = df['zScore'] > short
    df['short_exit'] = df['zScore'] < 0

    df['positions_short'] = np.nan
    df.loc[df.short_entry, 'positions_short'] = -1
    df.loc[df.short_exit, 'positions_short'] = 0

    df.positions_short = df.positions_short.fillna(method='ffill')

    # Positions
    df['positions'] = df.positions_long + df.positions_short

    return df

#assets_close

#b = assets_close[['PETR3','PETR4']]
#b = b.loc['2022-01-01':]
#b['spread'] = b.PETR3 - 1.13368 * b.PETR4

#b = aZ_score(b, 23, -1.680746546515109, 1.618126154507451)

#b = pd.read_csv(r'C:\Users\Fabio\PycharmProjects\pythonProject\Pair_intra_IBOV\csv_file\PETR3.csv', index_col='time')