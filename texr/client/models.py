class User(object):
    def __init__(self, login, name):
        self.login = login
        self.name = name

class Call(object):
    def __init__(self, cid, cdir, cstate, ts, remote):
        self.cid = cid
        self.dir = cdir
        self.state = cstate
        self.ts = ts
        self.remote = remote

    def accept(self):
        self._ipc.control_call(self.cid, 0)

    def hang(self):
        self._ipc.control_call(self.cid, 1)

    def established(self):
        pass

    def __repr__(self):
        sdir = "to" if self.dir else "from"
        return "<Call %s %s>" %(sdir,self.remote.login,)

