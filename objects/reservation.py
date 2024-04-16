import json
import os
from dotenv import load_dotenv
import time
import requests
import urllib
import datetime
from main import app


load_dotenv(override=True)

class Reservation:

    def __init__(self, venue_id, template_id, service_id, reservation_date, reservation_time, party_size, table_type, email, auth_token, payment_method_id):
        self.venue_id = venue_id
        self.template_id = template_id
        self.service_id = service_id
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.party_size = party_size
        self.table_type = table_type
        self.email = email
        self.auth_token = auth_token
        self.payment_method_id = payment_method_id
        self.reservation_token = None
        self.request_duration = None
        self.executed_at = None
        self.created_token = False
        self.got_reservation = False
        self.error_headers = None
        self.error_body = None

    @staticmethod
    @app.task
    def get_token(self):
        url = "https://api.resy.com/3/details"
        data = json.dumps({
            "commit": 1,
            "config_id": f"rgs://resy/{self.venue_id}/{self.template_id}/{self.service_id}/{self.reservation_date}/{self.reservation_date}/{self.reservation_time}/{self.party_size}/{self.table_type}",
            "day": self.reservation_date,
            "party_size": self.party_size
        })
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'ResyAPI api_key="{os.getenv('RESY_API_KEY')}"',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        try:
            res = requests.post(url, headers=headers, data=data)
            status = res.status_code
            response_headers = res.headers
            body = res.content
            
            if status == 201:
                json_body = json.loads(body)
                self.reservation_token = urllib.parse.quote(json_body['book_token']['value'])
                self.created_token = True
            elif 'X-Cache' in response_headers and response_headers['X-Cache'] == 'Error from cloudfront':
                print(f"Cloudfront Error - Max Requests Reached")
            else:
                print(f'unexpected response: {body.decode()}')
        except Exception as e:
            print(f'error generating reservation token: {e}')
    
    @staticmethod
    @app.task
    def book(self):
        url = "https://api.resy.com/3/book"
        # Define the payload for the booking request
        data = {
            "book_token": self.reservation_token,
            "struct_payment_method": json.dumps({"id": self.payment_method_id}),
            "source_id": "resy.com-venue-details"
        }
        # Define the headers for the booking request
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'ResyAPI api_key="{os.getenv('RESY_API_KEY')}"',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-resy-auth-token': self.auth_token,
            'x-resy-universal-auth': self.auth_token
        }

        # Synchronous POST request using requests library
        try:
            request_start = time.perf_counter_ns()
            executed_at = datetime.datetime.now()
            response = requests.post(url, headers=headers, data=data)
            request_end = time.perf_counter_ns()
            self.request_duration = int((request_end - request_start) / 1000000)
            self.executed_at = executed_at

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

        except Exception as e:
            print(f"Post request failure: {e}")
            self.error_body = str(e)
