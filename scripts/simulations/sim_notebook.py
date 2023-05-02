import requests
import utils

latlong = utils.get_random_fer_lat_lon()

payload = {
    "source_type": "notebook",
    "source_id": utils.get_random_hostname(),
    "latitude": latlong[0],
    "longitude": latlong[1],
    "timestamp": utils.get_timestamp()
}
url = utils.get_alerts_endpoint()
response = requests.post(url, json=payload,verify=False)