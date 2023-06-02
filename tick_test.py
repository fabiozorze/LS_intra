import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from datetime import datetime
import time



global connection
connection = False
if not mt5.initialize():
    connection = False
    print("initialize() fail")
    mt5.shutdown()
connection = True
print(connection)

dt = datetime.now()
df = pd.DataFrame()

while True:
    time.sleep(10)
    dt = datetime.now()
    if (dt.hour == 18) & (dt.minute > 0):
        tick = mt5.symbol_info_tick('PETR4')

        tick_data = {
                'Time': pd.to_datetime(tick.time, unit='s'),
                'Bid': tick.bid,
                'Ask': tick.ask,
                'Last': tick.last,
                'Volume': tick.volume,
                'Time_ms': tick.time_msc,
                'Flags': tick.flags,
                'Volume_Real': tick.volume_real
            }
        u = pd.DataFrame([tick_data])

        df = pd.concat([df, pd.DataFrame(u, index=[0])], ignore_index=True)


    if (dt.hour == 18) & (dt.minute > 31):
        df.to_csv(r'C:\Users\Fabio\PycharmProjects\pythonProject\Pair_intra_IBOV\tick_test_data\test.csv')
        break


