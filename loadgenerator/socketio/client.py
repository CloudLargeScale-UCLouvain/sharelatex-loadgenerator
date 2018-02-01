import time
import uuid
from websocket import create_connection
from .packet import encode, decode
from urlparse import urlparse

from locust.events import request_success

DEBUG=False

def debug(msg):
    if DEBUG: print(msg)

current_milli_time = lambda: int(round(time.time() * 1000))

class Client():
    def __init__(self, locust):
        self.hooks = {}
        self.req_track={}
        self.wsdict = {'clientTracking.updatePosition':'update_cursor_position', 'applyOtUpdate':'update_text'}
        base_url = urlparse(locust.client.base_url)
        resp = locust.client.get("/socket.io/1/",
                                 params={"t": int(time.time()) * 1000},
                                 name="get_socket.io")
        fields = resp.content.split(":")
        assert len(fields) == 4, ("unexpected response for socketio handshake: '%s'" % resp.content)
        url = "ws://%s/socket.io/1/websocket/%s" % (base_url.netloc, fields[0])
        headers = {"Cookie": resp.request.headers["Cookie"]}
        self.ws = create_connection(url, header=headers)
        m,_ = self._recv()
        assert m["type"] == "connect"

    def _recv(self):
        start_at = time.time()
        res = self.ws.recv()
        debug("<< " + res)
        data = decode(res)
        name = data.get("name", "")
        # request_success.fire(request_type='WebSocketRecv',
        #         name="socket.io/%s#%s" % (name,data["type"]),
        #         response_time=int((time.time() - start_at) * 1000000),
        #         response_length=len(res))
        return data, len(res)

    def _send(self, pkt):
        start_at = time.time()
        msg = encode(pkt)
        debug(">> " + msg)
        self.ws.send(msg)
        # request_success.fire(
        #         request_type='WebSocketSent',
        #         name="socket.io/%s#%s" % (pkt.get("name", ""), pkt["type"]),
        #         response_time=int((time.time() - start_at) * 1000000),
        #         response_length=len(msg))

    def emit(self, name, args, id=None, add_version=False):
        args_i=[k for k,v in enumerate(args) if type(v) is dict]
        if args_i:
            client_ts = current_milli_time()
            client_rid = str(uuid.uuid4().hex)
            args[args_i[0]]['client_ts'] = client_ts
            args[args_i[0]]['client_rid'] = client_rid
            nm = self.wsdict[name] if name in self.wsdict else name
            self.req_track[client_rid] = dict(name=nm, req_ts=client_ts)
        pkt = {"ack": "data", "type": "event", "name": name, "args": args}
        if id is not None:
            pkt["id"] = id
        self._send(pkt)

    def on(self, event, callback):
        self.hooks[event] = callback

    def recv(self):
        while True:
            r, rlen = self._recv()
            debug(r)
            if r["type"] == "heartbeat":
                self._send({"type": "heartbeat"})
            elif r["type"] == "event" and r["name"] in self.hooks:
                debug("trigger hook")
                if r["args"] and type(r["args"][0]) is dict and 'client_rid' in r["args"][0]:
                    client_rid = r["args"][0]['client_rid']
                    client_ts = current_milli_time()
                    if client_rid in self.req_track:
                        self.req_track[client_rid]['res_ts'] = client_ts
                        request_success.fire(request_type='WebSocket',
                            name="%s" % self.req_track[client_rid]['name'],
                            response_time=client_ts - self.req_track[client_rid]['req_ts'],
                            response_length=rlen)
                        del self.req_track[client_rid]

                self.hooks[r["name"]](r["args"])
            else:
                return r

    def close(self):
        self.ws.close()
