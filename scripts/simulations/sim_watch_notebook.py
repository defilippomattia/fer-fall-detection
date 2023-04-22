import requests
import utils
import time
num_watch_requests = 5
num_notebook_requests = 5

notebook_payload = {
    "source_type": "notebook",
    "source_id": "",
    "longitude": "",
    "latitude": "",
    "timestamp": ""
}

watch_payload = {
    "specversion":"1.0",
    "id":"bd4145c3-ec0e-4406-b419-4a770a699987",
    "source":"/v1/messages/receive",
    "type":"message.phone.received",
    "datacontenttype":"application/json",
    "time":"2023-04-06T05:20:30.442496539Z",
    "data":{
       "message_id":"95fef2ad-b869-464b-b465-8d5509eed696",
       "user_id":"3plicnuYmdTyh9GyPOHG2m0eARh1",
       "owner":"",
       "contact": "",
       "timestamp":"",
       "content":"",
       #"content":f"My current location: http://maps.google.com/maps?q={utils.get_random_lat()},{utils.get_random_lon()}",
       "sim":"DEFAULT"
    }
}

url = utils.get_alerts_endpoint()

for i in range(num_notebook_requests):
    latlong = utils.get_random_fer_lat_lon()
    notebook_payload["source_id"] = utils.get_random_hostname()
    notebook_payload["latitude"] = latlong[0]
    notebook_payload["longitude"] = latlong[1]
    notebook_payload["timestamp"] = utils.get_timestamp()
    time.sleep(utils.get_random_sleep())
    response = requests.post(url, json=notebook_payload)

for i in range(num_watch_requests):
    latlong = utils.get_random_fer_lat_lon()
    watch_payload["data"]["owner"] = utils.get_random_phone_num()
    watch_payload["data"]["contact"] = utils.get_random_phone_num()
    watch_payload["data"]["timestamp"] = utils.get_timestamp()
    watch_payload["data"]["content"] = f"My current location: http://maps.google.com/maps?q={latlong[0]},{latlong[1]}"
    time.sleep(utils.get_random_sleep())
    response = requests.post(url, json=watch_payload)

