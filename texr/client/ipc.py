import time
import os
import msgpack
import socket

class IPC(object):
    CALL_IN = 0
    CALL_OUT = 1

    REG_OFFLINE = 0
    REG_ONLINE = 4
    REG_TRY = 5

    OP_ACCEPT = 0
    OP_HANG = 1

    def __init__(self, socket_path):
        self.handlers = []
        self.delayed = []
        sock = socket.socket(1, socket.SOCK_STREAM)

        self.socket_path = socket_path

        try:
            sock.connect(socket_path)
            self.sock = sock
        except socket.error:
            self.sock = None
            print 'no socket, need to spawn driver'
            try:
                os.unlink(socket_path)
            except:
                pass

    def late_connect(self):

        while not os.access(self.socket_path, 0):
            print 'waiting for socket', self.socket_path
            time.sleep(1)

        sock = socket.socket(1, socket.SOCK_STREAM)
        sock.connect(self.socket_path)
        self.sock = sock
        buf_list = self.delayed
        self.delayed = []
        map(self.sock.send, buf_list)

    def add_handler(self, f):
        assert callable(f)
        self.handlers.append(f)

    def send(self, *args):
        buf = msgpack.packb(list(args))
        if self.sock is None:
            self.delayed.append(buf)
            return

        self.sock.send(buf)

    def loop(self):
        unpacker = msgpack.Unpacker()

        if self.sock is None:
            self.late_connect()

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
        assert isinstance(login ,basestring)
        self.send("sip.me", login)

    def set_online(self, state):
        assert isinstance(state, int)
        self.send("sip.online", state)

    def login_phone(self, phone):
        assert isinstance(phone, basestring) and phone
        self.send("api.login_phone", phone)

    def signup(self, token, otp, login, name):
        assert isinstance(token, basestring) and token
        assert isinstance(otp, basestring) and otp

        assert isinstance(login, basestring) and login
        assert isinstance(name, basestring) and name
        self.send('api.signup', token, otp, login, name)

    def send_login(self, login, password):
        assert isinstance(login, basestring) and login
        assert isinstance(password, basestring) and password
        self.send("cert.get", login, password)

    def control_call(self, cid, op):
        assert isinstance(cid, basestring) and cid
        assert isinstance(op, int)

        self.send("sip.call.control", cid, op)

    def place_call(self, login, name):
        assert isinstance(login, basestring) and login
        assert isinstance(name, basestring) and name

        self.send("sip.call.place", login, name)

    def send_message(self, login, text):
        assert isinstance(login, basestring) and login
        assert isinstance(text, basestring) and text

        self.send('message.send', login, text)

    def fetch_history(self, flag):
        self.send("hist.fetch", flag)

    def fetch_contacts(self,):
        self.send("contacts.fetch",)
