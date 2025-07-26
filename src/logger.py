import threading

class YdlLogger(object):
    def __init__(self, downloads, download_id):
        self.downloads = downloads
        self.download_id = download_id
        self.lock = threading.Lock()
    
    def debug(self, msg):
        with self.lock:
            self.downloads["log"] += f"{msg}\n"
        
    def warning(self, msg):
        with self.lock:
            self.downloads["log"] += f"[color=ffff00]{msg}[/color]\n"
    
    def error(self, msg):
        with self.lock:
            self.downloads["log"] += f"[color=ff0000]{msg}[/color]\n"
