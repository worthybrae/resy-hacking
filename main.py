from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv(override=True)


def initialize(reservation_time):
    oyster = MongoClient(os.getenv('MONGO_URL'))
    oyster = oyster['oyster']
    profiles = get_profiles(oyster)
