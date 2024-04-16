import datetime
import time
import requests


def make_post_request(url, headers, data, logger):
    try:
        execution_timestamp = datetime.datetime.now()
        request_start = time.perf_counter_ns()

        # Synchronous POST request using requests library
        res = requests.post(url, data=data, headers=headers)

        request_end = time.perf_counter_ns()
        request_duration = int((request_end - request_start) / 1000000)
        status = res.status_code
        response_headers = res.headers
        body = res.content  # Gets the response body

        return status, response_headers, body, execution_timestamp, request_duration
    except Exception as e:
        logger.error(f"post request failure: {e}")
        return None, None, None, None, None