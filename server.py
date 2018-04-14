from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from pythonosc import dispatcher
from pythonosc import osc_server
import queue
import json
import time

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



class OscObject:
    def __init__(self, c, d, t, a, b, g):
        self.channel = c
        self.delta = d
        self.theta = t
        self.alpha = a
        self.beta = b
        self.gamma = g

class OscSender:
    """ Listens on OSC port and sends the data to a websocket. """
    def __init__(self, osc_url, osc_ip, osc_port, web_socket):
        self._osc_url = osc_url
        self._osc_ip = osc_ip
        self._osc_port = osc_port
        self._web_socket = web_socket
        self._register = queue.Queue(maxsize=4)

    def handle_data(self, _, c, d, t, a, b, g):
        time.sleep(0.1)
        if c < self._register.qsize():
            objs = list()
            while not self._register.empty():
                objs.append(self._register.get())
            objs.append(OscObject(c,d,t,a,b,g))
            # send the array of osc objects here over the websocket
        else:
            self._register.put(OscObject(c,d,t,a,b,g))

    def run(self):
        dispatch = dispatcher.Dispatcher()
        dispatch.map(self._osc_url, self.handle_data)
        server = osc_server.ThreadingOSCUDPServer((self._osc_ip, self._osc_port), dispatch)
        print("Serving now")
        server.serve_forever()
"""
if __name__ == "__main__":
    sender = OscSender("/openbci", "127.0.0.1", 12345, None)
    sender.run()
"""

if __name__ == '__main__':
    socketio.run(app)
