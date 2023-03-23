from datetime import datetime
import time
import pandas as pd
import MetaTrader5 as mt5
from time import sleep
import Principal as pri

import numpy as np
import os



global connection
connection = False
if not mt5.initialize():
    connection = False
    print("initialize() fail")
    mt5.shutdown()
connection = True
print(connection)

assets = pd.read_csv(r'C:\Users\Fabio\PycharmProjects\pythonProject\Pair_intra_IBOV\2022.csv')[['y', 'x']]
assets_list = assets[['y', 'x']].values.tolist()
assets_list = [item for sublist in assets_list for item in sublist]

q = 0
data = pd.DataFrame()
data_one = pd.DataFrame()
sim = True
minute_old = 1


if __name__ == '__main__':

    contando = 0
    # BLOCK TO DOWNLOAD HALLIFE BACK OF DATA
    while True:
        dt = datetime.now()
        #print (dt.minute % 5)

        if dt.minute % 5 == 0:
            break

    assets_close = pd.DataFrame()
    for ASSET in assets_list:
        assets_close[ASSET] = pd.DataFrame(mt5.copy_rates_from_pos(ASSET, mt5.TIMEFRAME_M5, 0, 250))[
            ['time', 'close']].set_index('time')[:-1]

    assets_close.index = pd.to_datetime(assets_close.index, unit='s')

    while q < 1:
        dt = datetime.now()
        mt = dt.strftime('%H:%M:%S')

        if dt.second > dt.second - 1:

            for asset in assets_list:
                y = pd.DataFrame(mt5.copy_rates_from_pos(asset, mt5.TIMEFRAME_M1, 0, 1))[['time', 'close']].set_index('time')
                data_one[asset] = y

                if asset == 'VALE3':
                    data = pd.concat([data, data_one], axis=0, ignore_index=False)
                    data_one = pd.DataFrame()

            time.sleep(1)

        if (dt.minute % 5 == 0) & (sim == True):
            data.index = pd.to_datetime(data.index, unit='s')
            data = data.resample('5t').last().dropna()

            assets_close = pd.concat([assets_close, data], axis=0, ignore_index=False).fillna(method="ffill")
            st_list = pri.Run_strategy(assets_close=assets_close)

            # SAVE ST DATAFRAMES TO EACH TXT FILE
            for l in st_list:
                df = l

                dir_name = r"C:\Users\Fabio\PycharmProjects\pythonProject\Pair_intra_IBOV"
                base_filename = df.columns[0] + ".txt"

                path = os.path.join(dir_name, base_filename)

                with open(path, 'a') as f:
                    f.truncate(0)
                    df_string = df.to_string(header=True, index=True)
                    f.write(df_string)


            #print(assets_close.iloc[-50:])
            minute_old = dt.minute
            sim = False
            data = pd.DataFrame()
            contando +=1

        if dt.minute != minute_old:
            sim = True


        if dt.hour == 20:
            break


assets_close['PETR4'] = np.nan

print (assets_close)