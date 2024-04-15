import datetime
import time


async def make_post_request(session, url, headers, data, logger):
    try:
        execution_timestamp = datetime.datetime.now()
        request_start = time.perf_counter_ns()
        async with session.post(url, data=data, headers=headers) as res:
            request_end = time.perf_counter_ns()
            request_duration = int((request_end - request_start) / 1000000)
            status = res.status
            headers = res.headers
            body = await res.read()
            return status, headers, body, execution_timestamp, request_duration
    except Exception as e:
        logger.error(f"post request failure: {e}")
        return None, None, None, None, None
