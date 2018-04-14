from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import jsonpickle

app = Flask(__name__)

socketio = SocketIO(app)

@socketio.on('connect')
def client_connected():
    print("Client connected")


@socketio.on('disconnect')
def client_disconnected():
    print("Client disconnected")


@app.route("/", methods=['POST'])
def data_recieved():
    data = request.get_json(force=True)
    socketio.emit('message', jsonpickle.dumps(data), json=True, broadcast=True)
    return "success"

if __name__ == '__main__':
    print("sockets listening")
    socketio.run(app, port=5000)
