from helpers.requests import make_post_request
import urllib
import json
import requests
import os
from dotenv import load_dotenv


load_dotenv(override=True)

def get_auth_token(email, password):
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
    response = requests.post("POST", "/3/auth/password", payload, headers)
    
    status = response.status_code
    response_headers = response.headers
    body = response.content.decode('utf-8')  # decode body to string from bytes
    
    if status == 201:
        print(f"profile {self.email} just got a reservation {self.venue_id} | {self.table_type} | {self.party_size} | {self.reservation_date}")
        self.got_reservation = True
    else:
        print(f"error reserving table: {body}")
        self.error_body = body
        self.error_headers = response_headers

    json_body = json.loads(data.decode("utf-8"))
    print(json_body)
    auth = json_body['token']
    return auth
