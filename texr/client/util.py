def cmd(name):
    def cmd(f):
        f._cmd_name = name
        return f
    return cmd


