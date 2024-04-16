import datetime
from celery import Celery
import requests
import json
import urllib
import os
from dotenv import load_dotenv
import time


load_dotenv(override=True)

app = Celery(
    'main',
    worker_pool='gevent',  # Use Gevent as the execution pool
    worker_concurrency=20
)
app.config_from_object('celery_config')
app.conf.beat_schedule = {
    'status_check': {
        'task': 'main.status_check',
        'schedule': 60.0
    }
}

from objects.profile import Profiles
from objects.reservation import Reservation
from helpers.database import get_restaurants, get_tables


def status_check():
    now = datetime.datetime.now()
    if now > datetime.datetime(year=now.year, month=now.month, day=now.day, hour=8, minute=0, second=0):
        initialize(540)

@app.task
def get_token(res):
    url = "https://api.resy.com/3/details"
    data = json.dumps({
        "commit": 1,
        "config_id": f"rgs://resy/{res.venue_id}/{res.template_id}/{res.service_id}/{res.reservation_date}/{res.reservation_date}/{res.reservation_time}/{res.party_size}/{res.table_type}",
        "day": res.reservation_date,
        "party_size": res.party_size
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'ResyAPI api_key="{os.getenv('RESY_API_KEY')}"',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    try:
        re = requests.post(url, headers=headers, data=data)
        status = re.status_code
        response_headers = re.headers
        body = re.content
        
        if status == 201:
            json_body = json.loads(body)
            res.reservation_token = urllib.parse.quote(json_body['book_token']['value'])
            res.created_token = True
        elif 'X-Cache' in response_headers and response_headers['X-Cache'] == 'Error from cloudfront':
            print(f"Cloudfront Error - Max Requests Reached")
        else:
            print(f'unexpected response: {body.decode()}')
    except Exception as e:
        print(f'error generating reservation token: {e}')
    return res

@app.task
def book(res):
    url = "https://api.resy.com/3/book"
    # Define the payload for the booking request
    data = {
        "book_token": res.reservation_token,
        "struct_payment_method": json.dumps({"id": res.payment_method_id}),
        "source_id": "resy.com-venue-details"
    }
    # Define the headers for the booking request
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'ResyAPI api_key="{os.getenv('RESY_API_KEY')}"',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-resy-auth-token': res.auth_token,
        'x-resy-universal-auth': res.auth_token
    }

    # Synchronous POST request using requests library
    try:
        request_start = time.perf_counter_ns()
        executed_at = datetime.datetime.now()
        response = requests.post(url, headers=headers, data=data)
        request_end = time.perf_counter_ns()
        res.request_duration = int((request_end - request_start) / 1000000)
        res.executed_at = executed_at

        status = response.status_code
        response_headers = response.headers
        body = response.content.decode('utf-8')  # decode body to string from bytes

        if status == 201:
            print(f"profile {res.email} just got a reservation {res.venue_id} | {res.table_type} | {res.party_size} | {res.reservation_date}")
            res.got_reservation = True
        else:
            print(f"error reserving table: {body}")
            res.error_body = body
            res.error_headers = response_headers

    except Exception as e:
        print(f"Post request failure: {e}")
        res.error_body = str(e)
    return res

def initialize(reservation_mins):
    # Create profiles object
    profiles_obj = Profiles()
    # Make sure profiles object is active
    if profiles_obj.active:
        # Randomly select 3 profiles
        profiles_obj.random_selection()
        # Update profile auth tokens
        profiles_obj.update_tokens()
        # Fetch retaraunt data from internal database
        restaraunts_data = get_restaurants(reservation_mins)
        # Get target venue ids
        venues = [x.venue_id for x in restaraunts_data[:3]]
        # Get table data from internal database
        tables_data = get_tables(venues)
        # Iterate through each profile
        for p in profiles_obj.profiles:
            # Iterate through each restaraunt
            for r in restaraunts_data[:3]:
                # Filter tables for each restaraunt
                filtered_tables = [t for t in tables_data if t.venue_id == r.venue_id and t.time_string in ['19:00:00', '19:30:00', '20:00:00']]
                # Check if reservation minutes is set for midnight
                if reservation_mins == 1440:
                    # If it is midnight add an extra day to our res date calculation
                    res_date = datetime.date.today() + datetime.timedelta(days=r.days_to_release + 1)
                else:
                    res_date = datetime.date.today() + datetime.timedelta(days=r.days_to_release)
                for t in filtered_tables[:3]:
                    resy = Reservation(
                        venue_id=r.venue_id,
                        template_id=t.template_id,
                        service_id=t.service_id,
                        reservation_date=res_date,
                        reservation_time=t.time_string,
                        party_size=t.party_size,
                        table_type=t.table_type,
                        email=p.email,
                        auth_token=p.auth_token,
                        payment_method_id=p.payment_method_id
                    )
                    resy = get_token.delay(resy)
                    resy.book.delay()

        



initialize(540)