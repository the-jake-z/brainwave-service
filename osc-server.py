from pythonosc import dispatcher
from pythonosc import osc_server
import requests
import queue
import time
import jsonpickle
from threading import Lock

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
        self._mutex = Lock()
        self._count = 0

    def handle_data(self, _, c, d, t, a, b, g):

        if c == 3 or c == 4:
            return

        self._mutex.acquire()
        try:
            self._count = (self._count + 1) % 19
        finally:
            self._mutex.release()

        if self._count == 0:
            requests.post("http://localhost:5000", data=jsonpickle.dumps(OscObject(c, d, t, a, b, g)))

    def run(self):
        dispatch = dispatcher.Dispatcher()
        dispatch.map(self._osc_url, self.handle_data)
        server = osc_server.ThreadingOSCUDPServer((self._osc_ip, self._osc_port), dispatch)
        print("Serving now")
        server.serve_forever()


def run_osc_app():
    print("starting osc app")
    sender = OscSender("/openbci", "127.0.0.1", 12349, None)
    sender.run()

if __name__ == '__main__':
    run_osc_app()
