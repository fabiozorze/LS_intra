from datetime import datetime
import time
import pandas as pd
import MetaTrader5 as mt5
from time import sleep

from pandas import DataFrame

global connection
connection = False
if not mt5.initialize():
    connection = False
    print("initialize() fail")
    mt5.shutdown()
connection = True
print(connection)

assets = pd.read_csv(r'C:\Users\Fabio\PycharmProjects\pythonProject\Pair_intra_IBOV\2022.csv')[['y', 'x']]
assets = assets[['y', 'x']].values.tolist()
assets = [item for sublist in assets for item in sublist]

q = 0
data = pd.DataFrame()
data_one = pd.DataFrame()
sim = True
minute_old = 1

if __name__ == '__main__':

    while q < 1:
        dt = datetime.now()
        mt = dt.strftime('%H:%M:%S')

        if dt.second > dt.second - 1:

            for asset in assets:
                y = pd.DataFrame(mt5.copy_rates_from_pos(asset, mt5.TIMEFRAME_M1, 0, 1))[['time', 'close']].set_index('time')
                #y.index = pd.to_datetime(y.index, unit='s')
                data_one[asset] = y
                #data = pd.concat([data, data_one], axis=0, ignore_index=False)
                # data = pd.concat([data, y], axis=0, ignore_index=False)

                if asset == 'VALE3':
                    data = pd.concat([data, data_one], axis=0, ignore_index=False)
                    #data.index = pd.to_datetime(data.index, unit='s')
                    data_one = pd.DataFrame()

            time.sleep(1)

        if (dt.minute % 5 == 0) & (sim == True):
            data.index = pd.to_datetime(data.index, unit='s')
            data = data.resample('5t').last().dropna()
            print(data.iloc[-50:])
            minute_old = dt.minute
            sim = False
            data = pd.DataFrame()

        if dt.minute != minute_old:
            sim = True

        if dt.hour == 20:
            break
