from flask import Flask, render_template, jsonify
import redis
import json
import time

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='20.105.195.145', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('alerts')

# Store all messages in a list
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_all_messages')
def get_all_messages():
    return jsonify({'messages': messages})

def update_messages():
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode()
            print(data)
            messages.append(json.loads(data))

# Start a separate thread to listen for updates
import threading
update_thread = threading.Thread(target=update_messages)
update_thread.start()


if __name__ == '__main__':
    app.run(port=6504, debug=False)
