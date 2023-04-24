from flask import Flask, render_template, Response
import redis
import json

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)
#r = redis.Redis(host='redis', port=6379, db=0)

pubsub = r.pubsub()
pubsub.subscribe('alerts')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def messages():
    print("entered messages")
    def generate():
        print("entered generate")
        for message in pubsub.listen():
            if message['type'] == 'message':
                payload = json.loads(message['data'].decode('utf-8'))
                print(f"Received message: {json.dumps(payload, indent=4)}")

                yield f"data: {json.dumps(payload)}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True,port=6504)