from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from logger import logger
from scheduler import scheduler
import art
import datetime


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info("The rooster has awoken")
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("The rooster has fallen asleep")
    scheduler.shutdown()


@app.get("/", response_class=PlainTextResponse)
async def root():
    logger.info("The rooster has been poked")
    rooster_art = art.text2art("Rooster")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_response = rooster_art + f'\n{current_time}'
    return full_response