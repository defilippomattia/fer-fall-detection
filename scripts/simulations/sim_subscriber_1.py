import redis
import json
# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

#subscrive to alerts channel
pubsub = r.pubsub()
pubsub.subscribe('alerts')

for message in pubsub.listen():
    if message['type'] == 'message':
        payload = json.loads(message['data'].decode('utf-8'))
        print(f"Received message: {json.dumps(payload, indent=4)}")