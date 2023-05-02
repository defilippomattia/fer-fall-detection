# from flask import Flask, render_template, Response
# import redis
# import json

# app = Flask(__name__)

# # Connect to Redis
# r = redis.Redis(host='20.105.195.145', port=6379, db=0)
# pubsub = r.pubsub()
# pubsub.subscribe('alerts')

# for message in pubsub.listen():
#     if message['type'] == 'message':
#         data = message['data'].decode()
#         print(data)


from flask import Flask, render_template, Response
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

@app.route('/stream')
def stream():
    def generate():
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode()
                yield f"data: {data}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6504, debug=True)
