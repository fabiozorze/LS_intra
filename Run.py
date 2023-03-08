#import Pair_intra_IBOV.Principal as pri
import Principal as pri
import MetaTrader5 as mt5
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


def run():

    scheduler = BackgroundScheduler(misfire_grace_time=3600, coalesce=True)
    #scheduler.start()

    trigger = CronTrigger(
        year="*", month="*", day="*", hour="*", minute="*/1", second="01"
    )
    scheduler.add_job(
        pri.Run_strategy,
        trigger=trigger
    )

    scheduler.start()


    while True:
        sleep(5)


if __name__ == '__main__':
    #pri.Run_strategy()
    run()
