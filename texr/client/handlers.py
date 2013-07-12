from app import app
from models import User, Call, History

@app.cmd("cert.ok")
def cert_ok(code, name=None):
    if code == 0:
        print 'logged in ok', name
        app.emit("login")
        app.online(True)
    else:
        app.interactive_login()

@app.event("login")
def fetch_history():
    app.fetch_history()

@app.cmd("hist.res")
def history_res(code, idx=None, data=None):
    if code != 0:
        print 'no history'
    else:
        history = map(History._make, data)
        app.add_history(history)
        app.fetch_history()

@app.cmd("sip.reg")
def reg_state(state):
    if state == 0:
        print 'reg failed, offline now'
    elif state == 5:
        print 'reg in progress...'
    elif state == 4:
        print 'online'
    else:
        print 'reg %d' %( state,)

@app.cmd("sip.call.add")
def add_call(cid, cdir, cstate, timestamp, name, login):
    remote = User(login=login, name=name)
    call_ob = Call(cid, cdir, cstate, timestamp, remote)
    call_ob._ipc = app.ipc

    app.add_call(call_ob)
    app.emit("call.add", call_ob)

@app.cmd("sip.call.del")
def del_call(cid, reason):
    call_ob = app.calls.get(cid)
    if call_ob is None:
        return

    app.remove_call(call_ob)
    app.emit("call.del", call_ob, reason)

@app.cmd("sip.call.est")
def est_call(cid):
    call_ob = app.calls.get(cid)
    if call_ob is None: 
        return

    call_ob.established()
    app.emit("call.est", call_ob)
