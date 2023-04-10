import requests
import utils

payload = {
    "specversion":"1.0",
    "id":"bd4145c3-ec0e-4406-b419-4a770a699987",
    "source":"/v1/messages/receive",
    "type":"message.phone.received",
    "datacontenttype":"application/json",
    "time":"2023-04-06T05:20:30.442496539Z",
    "data":{
       "message_id":"95fef2ad-b869-464b-b465-8d5509eed696",
       "user_id":"3plicnuYmdTyh9GyPOHG2m0eARh1",
       "owner":utils.get_random_phone_num(),
       "contact": utils.get_random_phone_num(),
       "timestamp":utils.get_timestamp(),
       "content":f"My current location: http://maps.google.com/maps?q={utils.get_random_lat()},{utils.get_random_lon()}",
       "sim":"DEFAULT"
    }
}

url = utils.get_alerts_endpoint()
response = requests.post(url, json=payload)