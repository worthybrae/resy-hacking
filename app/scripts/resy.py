from scripts.requests import make_post_request
import urllib
import json


async def get_reservation_token(session, token_seed, api_key, logger):

    url = "https://api.resy.com/3/details"

    data = json.dumps({
        "commit": 1,
        "config_id": f"rgs://resy/{token_seed['venue_id']}/{token_seed['template_id']}/{token_seed['service_id']}/{token_seed['reservation_date']}/{token_seed['reservation_date']}/{token_seed['reservation_time']}/{token_seed['party_size']}/{token_seed['table_type']}",
        "day": token_seed['reservation_date'],
        "party_size": token_seed['party_size']
    })

    # Define the headers for the request
    headers = {
        'authority': 'api.resy.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'ResyAPI api_key="{api_key}"',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://widgets.resy.com',
        'referer': 'https://widgets.resy.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-origin': 'https://widgets.resy.com'
    }

    status, headers, body, execution_timestamp, request_duration = await make_post_request(session, url, headers, data, logger)

    if status == 201:
        json_body = json.loads(body)
        token_seed['reservation_token'] = urllib.parse.quote(json_body['book_token']['value'])
    elif headers['X-Cache'] == 'Error from cloudfront':
        token_seed['reservation_token'] = None
        logger.error(f"the reservation token can't be generated using your token seed: {token_seed['venue_id']} | {token_seed['table_type']} | {token_seed['party_size']} | {token_seed['reservation_date']} {token_seed['reservation_time']}")
    else:
        token_seed['reservation_token'] = None
        logger.error(f'unexpected response: {body}')
    return token_seed


async def get_reservation(session, reservation_seed, api_key, logger):
    # Define the URL
    url = "https://api.resy.com/3/book"

    # Define the payload for the booking request
    data = f"book_token={reservation_seed['reservation_token']}&struct_payment_method=%7B%22id%22%3A{reservation_seed['payment_method_id']}%7D&source_id=resy.com-venue-details"

    # Define the headers for the booking request
    headers = {
        'authority': 'api.resy.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'ResyAPI api_key="{api_key}"',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://widgets.resy.com',
        'referer': 'https://widgets.resy.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-origin': 'https://widgets.resy.com',
        'x-resy-auth-token': reservation_seed['auth_token'],
        'x-resy-universal-auth': reservation_seed['auth_token']
    }

    status, headers, body, execution_timestamp, request_duration = await make_post_request(session, url, headers, data, logger)

    reservation_seed['request_duration'] = request_duration
    reservation_seed['execution_timestamp'] = execution_timestamp
    if status == 201:
        logger.info(f"profile {reservation_seed['profile_id']} just got a reservation {reservation_seed['venue_id']} | {reservation_seed['table_type']} | {reservation_seed['party_size']} | {reservation_seed['reservation_timestamp']}")
        reservation_seed['outcome'] = True
        reservation_seed['error_body'] = None
        reservation_seed['error_headers'] = None
        return reservation_seed
    else:
        logger.error(f"error reserving table: {body}")
        reservation_seed['outcome'] = False
        reservation_seed['error_body'] = body
        reservation_seed['error_headers'] = headers
        return reservation_seed


