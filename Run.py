#import Pair_intra_IBOV.Principal as pri
import Principal as pri
import MetaTrader5 as mt5
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


def check_allowed_trading_hours():
    if 13 <= datetime.now().hour < 21:
        return True
    else:
        return False


if __name__ == '__main__':
    #pri.Run_strategy()
    run()

            if datetime.now().hour != hour_check:
                time.sleep(5)
                print(datetime.now().hour, hour_check)

            if (datetime.now().minute % 5 == 0) & (contando == 0) & (new_hour == True):
                pri.Run_strategy()
                contando = 1
                old_hour = datetime.now().minute
                new_hour = False
                print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


            elif datetime.now().minute != old_hour:
                new_hour = True
                contando = 0

        time.sleep(5)