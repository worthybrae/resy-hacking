from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logger import logger
from pytz import timezone
from scripts.main import initialize
from dotenv import load_dotenv


load_dotenv(override=True)
scheduler = AsyncIOScheduler()


async def nine_am():
    minutes_to_release = 540
    lag = 2
    rate = 5
    volume = 2000
    logger.info("cock a doodle doo its 9am")
    results = await initialize(minutes_to_release, lag, rate, volume, logger)


async def ten_am():
    minutes_to_release = 600
    lag = 2
    rate = 5
    volume = 2000
    logger.info("cock a doodle doo its 10am")
    results = await initialize(minutes_to_release, lag, rate, volume, logger)


async def midnight():
    minutes_to_release = 1440
    lag = 2
    rate = 5
    volume = 2000
    logger.info("cock a doodle doo its midnight")
    results = await initialize(minutes_to_release, lag, rate, volume, logger)


scheduler.add_job(nine_am, 'cron', hour=8, minute=50, timezone=timezone('US/Eastern'))
scheduler.add_job(ten_am, 'cron', hour=9, minute=50, timezone=timezone('US/Eastern'))
scheduler.add_job(midnight, 'cron', hour=23, minute=50, timezone=timezone('US/Eastern'))