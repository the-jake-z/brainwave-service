from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

socketio = SocketIO(app)


@socketio.on('connect')
def client_connected():
    print("Client connected")


@socketio.on('disconnect')
def client_disconnected():
    print("Client disconnected")


def send_data(data):
    send(data)

if __name__ == '__main__':
    socketio.run(app)
