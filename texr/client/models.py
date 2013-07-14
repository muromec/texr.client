from collections import namedtuple
import time

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

HistoryTuple = namedtuple("History", ['event', 'ts', 'key', 'login', 'name'])
class History(HistoryTuple):
    HIST_OUT=(1<<1)
    HIST_IN=(1<<2)
    HIST_OK=(1<<3)
    HIST_HANG=(1<<4)
    HIST_CONTACT=(1<<5)
    HIST_CONTACT_RM=(1<<7)
    HIST_CONTACT_ADD=(1<<8)

    def __repr__(self):
        cdir = self.cdir
        return '<History %s %s at %s>' % (cdir, self.login, self.time_str)

    @property
    def cdir(self):
        if self.event & self.HIST_IN:
            return 'from'
        if self.event & self.HIST_OUT:
            return 'to'

        return 'wtf'

    @property
    def time_str(self):
        ts = time.localtime(self.ts)
        return time.asctime(ts)

ContactTuple = namedtuple("Contact", ['login', 'name', 'phone'])

class Contact(ContactTuple):
    def __repr__(self):
        return '<C: %s (%s)>' %(self.name, self.login)
