from flask import Flask, render_template, jsonify
import redis
import json

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='20.105.195.145', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('alerts')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def messages():
    messages = []

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode()
            print(type(data))
            a = json.loads(data)
            print(type(a))
            messages.append(a)
            return jsonify(messages)

if __name__ == '__main__':
    app.run(port=6504, debug=False)
