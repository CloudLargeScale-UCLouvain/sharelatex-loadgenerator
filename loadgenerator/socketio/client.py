import time
from websocket import create_connection
from .packet import encode, decode
from urlparse import urlparse

from locust.events import request_success

class Client():
    def __init__(self, locust):
        self.hooks = {}
        url = urlparse(locust.client.base_url)
        resp = locust.client.get("/socket.io/1/",
                                 params={"t": int(time.time()) * 1000},
                                 name="/socket.io/1/t=[ts]")
        fields = resp.content.split(":")
        assert len(fields) == 4, ("unexpected response for socketio handshake: '%s'" % resp.content)
        url = "ws://%s/socket.io/1/websocket/%s" % (url.netloc, fields[0])
        headers = {"Cookie": resp.request.headers["Cookie"]}
        self.ws = create_connection(url, header=headers)
        m = self._recv()
        assert m["type"] == "connect"

    def _recv(self):
        start_at = time.time()
        res = self.ws.recv()
        print("<< " + res)
        data = decode(res)
        name = data.get("name", "")
        request_success.fire(request_type='WebSocket Recv',
                name="socket.io/%s#%s" % (name,data["type"]),
                response_time=int((time.time() - start_at) * 1000000),
                response_length=len(res))
        return data

    def _send(self, pkt):
        start_at = time.time()
        msg = encode(pkt)
        print(">> " + msg)
        self.ws.send(msg)
        request_success.fire(
                request_type='WebSocket Sent',
                name="socket.io/%s#%s" % (pkt.get("name", ""), pkt["type"]),
                response_time=int((time.time() - start_at) * 1000000),
                response_length=len(msg))

    def emit(self, name, args, id=None, add_version=False):
        pkt = {"ack": "data", "type": "event", "name": name, "args": args}
        if id is not None:
            pkt["id"] = id
        self._send(pkt)

    def on(self, event, callback):
        self.hooks[event] = callback

    def recv(self):
        while True:
            r = self._recv()
            print(r)
            if r["type"] == "heartbeat":
                self._send({"type": "heartbeat"})
            elif r["type"] == "event" and r["name"] in self.hooks:
                print("trigger hook")
                self.hooks[r["name"]](r["args"])
            else:
                return r

    def close(self):
        self.ws.close()
