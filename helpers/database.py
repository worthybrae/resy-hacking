from dotenv import load_dotenv
import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from objects.table import Table
from objects.restaraunt import Restaraunt


load_dotenv(override=True)

def get_profiles():

    id = quote_plus(os.getenv('MONGO_ID'))
    db = quote_plus(os.getenv('MONGO_DB'))
    username = quote_plus(os.getenv('MONGO_USER'))
    password = quote_plus(os.getenv('MONGO_PASSWORD'))
    uri = f"mongodb+srv://{username}:{password}@{db}.{id}.mongodb.net/?retryWrites=true&w=majority&appName={db}"
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri)
        oyster = client['oyster']
        profiles = oyster['profiles'].find({})
    except Exception as e:
        print(f"error connecting to mongo: {e}")
        return None

    profiles_data = []
    
    for p in profiles:
        # Using dict.get() to avoid KeyError if the key doesn't exist
        try:
            data = {
                'password': p.get('password'),
                'email': p.get('email'),
                '_id': p.get('_id'),
                'auth_token': p.get('auth_token'),  # Provide a default value if key doesn't exist
                'payment_method_id': p.get('payment_method_id')
            }
            profiles_data.append(data)
        except Exception as e:
            print(f"error fetching data from mongo object: e")
    
    client.close()    
    return profiles_data

def get_restaurants(minutes_to_release):
    id = quote_plus(os.getenv('MONGO_ID'))
    db = quote_plus(os.getenv('MONGO_DB'))
    username = quote_plus(os.getenv('MONGO_USER'))
    password = quote_plus(os.getenv('MONGO_PASSWORD'))
    uri = f"mongodb+srv://{username}:{password}@{db}.{id}.mongodb.net/?retryWrites=true&w=majority&appName={db}"
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri)
        oyster = client['oyster']
        restaurants = oyster['restaurants'].find({'minutes_to_release': minutes_to_release})
        restaurants_data = [
            Restaraunt(
                venue_id = r['venue_id'],
                days_to_release = r['days_to_release'],
                minutes_to_release = r['minutes_to_release'],
                name = r['name']
            ) for r in restaurants
        ]
        return restaurants_data
    except Exception as e:
        print(f"error connecting to mongo: {e}")
        return None

def get_tables(venue_ids):
    id = quote_plus(os.getenv('MONGO_ID'))
    db = quote_plus(os.getenv('MONGO_DB'))
    username = quote_plus(os.getenv('MONGO_USER'))
    password = quote_plus(os.getenv('MONGO_PASSWORD'))
    uri = f"mongodb+srv://{username}:{password}@{db}.{id}.mongodb.net/?retryWrites=true&w=majority&appName={db}"
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri)
        oyster = client['oyster']
        tables = oyster['tables'].find({"venue_id": {"$in": venue_ids}})
        tables_data = [
            Table(
                venue_id = t['venue_id'],
                template_id = t['template_id'],
                service_id = t['service_id'],
                time_string = t['time_string'],
                party_size = t['party_size'],
                table_type = t['table_type'],
                id = t['_id']
            ) for t in tables
        ]
        return tables_data
    except Exception as e:
        print(f"database connection issue: {e}")
        return None