class YdlLogger(object):
    def __init__(self, data):
        self.data = data

    def debug(self, msg):
        self.data["log"] += f"{msg}\n"
        
    def warning(self, msg):
        self.data["log"] += f"[color=ffff00]{msg}[/color]\n"

    def error(self, msg):
        self.data["log"] += f"[color=ff0000]{msg}[/color]\n"
