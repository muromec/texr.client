import os
import msgpack
import socket

class IPC(object):

    def __init__(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        home = os.getenv("HOME")
        sock.connect("%s/.texr.sock" % (home,))
        self.handlers = []

        self.sock = sock

    def add_handler(self, f):
        assert callable(f)
        self.handlers.append(f)

    def send(self, *args):
        buf = msgpack.packb(list(args))
        self.sock.send(buf)

    def loop(self):
        unpacker = msgpack.Unpacker()
        while True:
            unpacker.feed(self.sock.recv(4096))
            for event in unpacker:
                if not event or not isinstance(event, list):
                    continue

                self.handle(*event)

    def handle(self, *event):
        for handler in self.handlers:
            try:
                handler(*event)
            except Exception as e:
                print  e

    def set_me(self, login):
        assert isinstance(login ,str)
        self.send("sip.me", login)

    def set_online(self, state):
        assert isinstance(state, int)
        self.send("sip.online", state)

    def send_login(self, login, password):
        assert isinstance(login, str) and login
        assert isinstance(password, str) and password
        self.send("cert.get", login, password)

    def control_call(self, cid, op):
        assert isinstance(cid, str) and cid
        assert isinstance(op, int)

        self.send("sip.call.control", cid, op)

    def fetch_history(self, flag):
        self.send("hist.fetch", flag)
