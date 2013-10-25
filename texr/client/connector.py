import os
from threading import Thread

from . ipc import IPC

class Connector(Thread):
  def __init__(self):
    self.fix_env()
    self.ipc = IPC(self.ipc_socket_path)
    if self.ipc.sock is None:
        self.spawn_driver()

    self.listeners = {}
    super(Connector, self).__init__()

  def fix_env(self):
    android_path = os.getenv('ANDROID_PRIVATE')
    self._is_android = bool(android_path)
    if not android_path:
        return

    os.setenv('HOME', android_path)
    assert os.path.exists(android_path)

  @property
  def driver_binary(self):
    if self._is_android:
      return self.android_driver_binary()

    here, _mod = os.path.split(__file__)
    return os.path.join(here, '..', 'texr-daemon')

  def android_driver_binary(self):
    android_path = os.getenv('ANDROID_PRIVATE')
    if android_path[-1] == '/':
        android_path = android_path[:-1]

    app_dir, _files = os.path.split(android_path)
    return os.path.join(app_dir, 'texr-daemon')

  @property
  def ipc_socket_path(self):
    if self._is_android:
        android_path = os.getenv('ANDROID_PRIVATE')
        return os.path.join(android_path, 'driver-sock')

    home = os.getenv('HOME')
    if home:
        return os.path.join(home, '.texr.sock')

    return '.texr.sock'

  def spawn_driver(self):
    dp = self.driver_binary
    if not os.access(dp, os.X_OK):
        raise OSError("driver binary not found at %r" % (dp,))

    ok = os.spawnl(os.P_NOWAIT, dp, 'texr-daemon', self.ipc_socket_path)
    print 'spawned driver', ok, dp, self.ipc_socket_path

  def run(self):
    print 'run here'
    self.ipc.add_handler(self.event)
    self.ipc.loop()

  def event(self, name, *args):
    print 'event', name, args
    for func in self.get_handlers(name):
      print func
      func(*args)

  def get_handlers(self, name):
    ipc_func = getattr(self, 'ipc_%s' % (name.replace('.', '_'),), None)
    if ipc_func and callable(ipc_func):
      yield ipc_func

    for lfunc in self.listeners.get(name, []):
      yield lfunc

  def listen_to(self, event, f):
    lfuncs = self.listeners.get(event, [])
    lfuncs.append(f)
    self.listeners[event] = lfuncs
