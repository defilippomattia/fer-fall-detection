import requests
import utils

payload = {
    "source_type": "notebook",
    "source_id": utils.get_random_hostname(),
    "longitude": utils.get_random_lon(),
    "latitude": utils.get_random_lat(),
    "timestamp": utils.get_timestamp()
}
url = utils.get_alerts_endpoint()
response = requests.post(url, json=payload)