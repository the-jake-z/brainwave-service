from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

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
    emit('message', data)

if __name__ == '__main__':
    print("sockets listening")
    socketio.run(app, port=5000)
