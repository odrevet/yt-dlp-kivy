import threading

class YdlLogger(object):
    def __init__(self, download, download_id):
        self.download = download
        self.lock = threading.Lock()
    
    def debug(self, msg):
        with self.lock:
            self.download["log"] += f"{msg}\n"
        
    def warning(self, msg):
        with self.lock:
            self.download["log"] += f"[color=ffff00]{msg}[/color]\n"
    
    def error(self, msg):
        with self.lock:
            self.download["log"] += f"[color=ff0000]{msg}[/color]\n"
