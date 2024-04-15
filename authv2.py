import http.client
import urllib
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv(override=True)

def get_profiles(oyster):
    try:
        # make query and process data
        profiles = oyster['profiles'].find({})
        profiles_data = [{
            '_id': p['_id'],
            'auth_token': p['auth_token'],
            'email': p['email'],
            'password': p['password']
        } for p in profiles]
        return profiles_data
    except Exception as e:
        print(f"database connection issue: {e}")
        return None
    

def update_profile(oyster, profile_id, auth_token):
    my_query = {'_id': profile_id}  

    # Set your new auth_token value
    new_values = {'$set': {'auth_token': auth_token}}  

    # Perform the update
    oyster['profiles'].update_one(my_query, new_values)
    

def get_auth_token(email, password):
    conn = http.client.HTTPSConnection("api.resy.com")
    payload = f'email={urllib.parse.quote(email)}&password={password}'
    headers = {
        'authority': 'api.resy.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'ResyAPI api_key="{os.getenv('RESY_API_KEY')}"',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://resy.com',
        'referer': 'https://resy.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-origin': 'https://resy.com'
    }
    conn.request("POST", "/3/auth/password", payload, headers)
    res = conn.getresponse()
    data = res.read()

    json_body = json.loads(data.decode("utf-8"))
    auth = json_body['token']
    return auth

def initialize():
    oyster = MongoClient(config('MONGO_URL'))
    oyster = oyster['oyster']
    profiles = get_profiles(oyster)
    for profile in profiles:
        print(profile['_id'], profile['auth_token'])
        tok = get_auth_token(profile['email'], profile['password'])
        print('\n')
        print(tok)
        update_profile(oyster, profile['_id'], tok)
        

initialize()