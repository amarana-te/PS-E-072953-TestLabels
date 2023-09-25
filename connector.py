import time
import logging
import requests.adapters
from datetime import datetime

super_http = requests.Session()
adapter1 = requests.adapters.HTTPAdapter(pool_connections=35, pool_maxsize=77)

super_http.mount('https://api.thousandeyes.com/', adapter=adapter1)


# Date & Time
def timestamp():
    date_time_now = datetime.now()
  
    return date_time_now.strftime("%m/%d/%H")

# Configure logging
logfile = timestamp().replace("/", "-").replace(":", "") + '-app.log'
logging.basicConfig(filename=logfile, level=logging.INFO)


def get_data(headers, endp_url):

    start = time.time()
    endpoint_data = super_http.get(url=endp_url, headers=headers)
    roundtrip = time.time() - start

    if endpoint_data.status_code == 429:

        dt_object = datetime.fromtimestamp(int(endpoint_data.headers.get('x-organization-rate-limit-reset'))) - datetime.now()
        time.sleep(dt_object.seconds + 1)
        endpoint_data = super_http.get(url=endp_url, headers=headers)

    else:
        info = "Status Code " + str(endpoint_data.status_code) + ": " + endp_url + " time: ", str(roundtrip)
        logging.info(info)

    endpoint_data = endpoint_data.json()

    return endpoint_data


def post_data(headers, endp_url, payload):

    start = time.time()
    endpoint_data = super_http.post(url=endp_url, headers=headers, data=payload)
    roundtrip = time.time() - start

    if endpoint_data.status_code == 429:

        dt_object = datetime.fromtimestamp(int(endpoint_data.headers.get('x-organization-rate-limit-reset'))) - datetime.now()
        time.sleep(dt_object.seconds + 1)
        endpoint_data = super_http.post(url=endp_url, headers=headers, data=payload)

        logging.info("Status Code " + str(endpoint_data.status_code) + ": " + endp_url + " time: " + str(roundtrip))
        return True

    elif endpoint_data.status_code == 400:

        logging.info("Status Code " + str(endpoint_data.status_code) + ": " + endp_url + " time: " + str(roundtrip))

        return False
    
    elif endpoint_data.status_code == 201:

        logging.info("Status Code " + str(endpoint_data.status_code) + ": " + endp_url + " time: " + str(roundtrip))
        return True

    else:

        logging.info("Status Code " + str(endpoint_data.status_code) + ": " + endp_url + " time: " + str(roundtrip))
        return False

    