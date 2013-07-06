from app import app

@app.event("call.add")
def have_call(call):
    if call.remote.login == 'ilya.muromec':
        call.accept()

@app.event("call.est")
def est_call(call):
    print 'call established', call

@app.event("call.del")
def del_call(call, reason):
    pass
