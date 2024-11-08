from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# REST endpoint


@app.route('/api/ocr', methods=['POST'])
def handle_message():
    data = request.json
    print(f"Received message: {data['message']}")
    return jsonify({"status": "Message received!"}), 200

# WebSocket event


@socketio.on('message')
def handle_socket_message(msg):
    print(f"Received socket message: {msg}")

    # Send "Hello" every second
    while True:
        socketio.send("Hello")
        socketio.sleep(1)  # Sleep for 1 second


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
