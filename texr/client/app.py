from ipc import IPC

class Texr(object):
    def __init__(self):
        self.ipc = IPC()
        self.ipc.add_handler(self.on_ipc)
        self.commands = {}
        self.event_handlers = {}
        self.calls = {}
        self.history = None

    def cmd(self, name):
        def cmd(f):
            self.commands[name] = f

        return cmd

    def event(self, name):
        def event(f):

            hlist = self.event_handlers.get(name) or []
            hlist.append(f)
            self.event_handlers[name] = hlist

        return event

    def on_ipc(self, name, *args):
        handler = self.commands.get(name)
        if handler is None:
            print 'unhandled %r' %(name,), args 
            return

        handler(*args)

    def run(self):
        self.ipc.loop()

    def me(self, login):
        self.ipc.set_me(login)

    def online(self, on):
        self.ipc.set_online(1 if on else 0)

    def interactive_login(self):
        import getpass
        login = raw_input("login: ")
        password = getpass.getpass("password: ")
        self.ipc.send_login(login, password)

    def add_call(self, call_ob):
        self.calls[call_ob.cid] = call_ob

    def remove_call(self, call_ob):
        try:
            del app.calls[call_ob.cid]
        except KeyError:
            return

    def fetch_history(self, reset=False):
        if reset:
            self.history = None

        self.ipc.fetch_history(1 if (self.history is None) else 0)
        self.history = []

    def add_history(self, data):
        print 'loaded %d' %(len(data),)
        self.history.extend(data)
        for entry in data:
            print entry

    def emit(self, name, *args):
        handlers = self.event_handlers.get(name, [])
        for handler in handlers:
            try:
                handler(*args)
            except Exception as e:
                print 'event handler failed', e


app = Texr()
