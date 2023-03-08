import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from datetime import datetime
import pytz

#import Pair_intra_IBOV.Order_modules as order
#import Pair_intra_IBOV.Strategy

import Order_modules as order
import Strategy


from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz



global connection
connection = False
if not mt5.initialize():
    connection = False
    print("initialize() fail")
    mt5.shutdown()

connection = True
print(connection)



def now():

    saopauloTz = pytz.timezone('Brazil/East')
    timeInSaoPaulo = datetime.now(saopauloTz)
    currentTimeInSaoPaulo = timeInSaoPaulo.strftime("%H:%M:%S")

    return print("The current time in New York is:", currentTimeInSaoPaulo)


def Run_strategy():
    selected = pd.read_csv(r'C:\Users\Fabio\PycharmProjects\pythonProject\Pair_intra_IBOV\2022.csv', index_col=[0])

    dfs = []

    for bar in range(len(selected)):
        pair = pd.DataFrame()
        Y = selected['y'][bar]
        X = selected['x'][bar]
        half = 20
        hedge_ratio = selected['hedge_ratio'][bar]
        short = selected['short'][bar]
        long = selected['long'][bar]

        y = pd.DataFrame(mt5.copy_rates_from_pos(Y, mt5.TIMEFRAME_H1, 0, 100))[['time', 'close']].set_index('time')
        x = pd.DataFrame(mt5.copy_rates_from_pos(X, mt5.TIMEFRAME_H1, 0, 100))[['time', 'close']].set_index('time')

        pair[Y] = y
        pair[X] = x
        pair['spread'] = y - hedge_ratio * x
        pair.index = pd.to_datetime(pair.index, unit='s')

        # RUN STRATEGY
        #st = Pair_intra_IBOV.Strategy.Z_score(pair, half, long, short)
        st = Strategy.Z_score(pair, half, long, short)
        print(st[-2:])
        st['hegde'] = hedge_ratio

        dfs.append(st)

        try:
            y_volume = mt5.positions_get(symbol=st.columns[0])[0][9]  # GET Y VOLUME
            x_volume = mt5.positions_get(symbol=st.columns[1])[0][9]  # GET X VOLUME
        except:
            y_volume = 0
            x_volume = 0

        # OPEN POSITION BLOCK
        if (y_volume == 0) & (x_volume == 0):
            if (st['positions'].iloc[-2] == 0):

                # OPEN SHORT_SPREAD POSITION
                if (st['positions'].iloc[-1] == -1):

                    print('---SHORT_POSITION---')
                    print(st.columns[0] + '-' + st.columns[1])

                    req1, req2 = order.Short(st.columns[0], st.columns[1], hedge_ratio, 1000000)
                    mt5.order_send(req1)
                    mt5.order_send(req2)

                # OPEN LONG_SPREAD POSITION
                elif (st['positions'].iloc[-1] == 1):

                    print('---LONG_POSITION---')
                    print(st.columns[0] + '-' + st.columns[1])

                    req1, req2 = order.Long(st.columns[0], st.columns[1], hedge_ratio, 1000000)
                    mt5.order_send(req1)
                    mt5.order_send(req2)

        else:

            if st['positions'].iloc[-1] == 0:

                # CLOSE SHORT SPREAD POSITON
                if (st['positions'].iloc[-2] == -1):

                    try:
                        y_volume = mt5.positions_get(symbol=st.columns[0])[0][9]  # GET Y VOLUME
                        x_volume = mt5.positions_get(symbol=st.columns[1])[0][9]  # GET X VOLUME
                    except:
                        y_volume = 0
                        x_volume = 0

                    if (y_volume != 0) & (x_volume != 0):
                        print('---CLOSE_SHORT_POSITION---')
                        print(st.columns[0] + '-' + st.columns[1])

                        sell, buy = order.Close_Short(st.columns[0], st.columns[1], y_volume, x_volume)
                        mt5.order_send(sell)
                        mt5.order_send(buy)

                # CLOSE LONG SPREAD POSITION
                elif (st['positions'].iloc[-2] == 1):

                    try:
                        y_volume = mt5.positions_get(symbol=st.columns[0])[0][9]  # GET Y VOLUME
                        x_volume = mt5.positions_get(symbol=st.columns[1])[0][9]  # GET X VOLUME
                    except:
                        y_volume = 0
                        x_volume = 0

                    if (y_volume != 0) & (x_volume != 0):
                        print('---CLOSE_LONG_POSITION---')
                        print(st.columns[0] + '-' + st.columns[1])

                        sell, buy = order.Close_Long(st.columns[0], st.columns[1], y_volume, x_volume)
                        mt5.order_send(sell)
                        mt5.order_send(buy)

            else:

                if (st['positions'].iloc[-2] == 1) & (st['positions'].iloc[-1] == -1):

                    try:
                        y_volume = mt5.positions_get(symbol=st.columns[0])[0][9]  # GET Y VOLUME
                        x_volume = mt5.positions_get(symbol=st.columns[1])[0][9]  # GET X VOLUME
                    except:
                        y_volume = 0
                        x_volume = 0

                    if (y_volume != 0) & (x_volume != 0):
                        print('---CLOSE_LONG_POSITION---')
                        print(st.columns[0] + '-' + st.columns[1])

                        sell, buy = order.Close_Long(st.columns[0], st.columns[1], y_volume, x_volume)
                        mt5.order_send(sell)
                        mt5.order_send(buy)

                        print('---SHORT_POSITION---')
                        print(st.columns[0] + '-' + st.columns[1])

                        req1, req2 = order.Short(st.columns[0], st.columns[1], hedge_ratio, 1000000)
                        mt5.order_send(req1)
                        mt5.order_send(req2)

                if (st['positions'].iloc[-2] == -1) & (st['positions'].iloc[-1] == 1):

                    try:
                        y_volume = mt5.positions_get(symbol=st.columns[0])[0][9]  # GET Y VOLUME
                        x_volume = mt5.positions_get(symbol=st.columns[1])[0][9]  # GET X VOLUME
                    except:
                        y_volume = 0
                        x_volume = 0

                    if (y_volume != 0) & (x_volume != 0):
                        print('---CLOSE_SHORT_POSITION---')
                        print(st.columns[0] + '-' + st.columns[1])

                        sell, buy = order.Close_Short(st.columns[0], st.columns[1], y_volume, x_volume)
                        mt5.order_send(sell)
                        mt5.order_send(buy)

                        print('---LONG_POSITION---')
                        print(st.columns[0] + '-' + st.columns[1])

                        req1, req2 = order.Short(st.columns[0], st.columns[1], hedge_ratio, 1000000)
                        mt5.order_send(req1)
                        mt5.order_send(req2)
    now()





#if __name__ == '__main__':
    #login()
    #Run_strategy()
    #now()


#st = dfs[-1]