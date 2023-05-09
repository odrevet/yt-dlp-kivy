import re


class YdlLogger(object):
    def __init__(self, data, lock):
        self.data = data
        self.lock = lock

    def debug(self, msg):
        m = re.search(
            r"^\[download\]\s+(\d+\.\d+)%\s+of\s+(\~?\s+\d+\.\d+\w+)\s+at\s+(\d+\.\d+\w+\/s)\s+ETA\s+(\d{2}:\d{2}).*",
            msg,
        )

        if m is not None:
            with self.lock:
                self.data["percent"] = float(m.group(1))
                self.data["file_size"] = m.group(2)
                self.data["speed"] = m.group(3)
                self.data["ETA"] = m.group(4)
        else:
            with self.lock:
                self.data["log"] += f"{msg}\n"
                if msg.endswith("has already been downloaded"):
                    self.data["percent"] = 100
                    self.data["ETA"] = "Video has alderly been downloaded"

    def warning(self, msg):
        with self.lock:
            self.data["log"] += f"[color=ffff00]{msg}[/color]\n"

    def error(self, msg):
        with self.lock:
            self.data["log"] += f"[color=ff0000]{msg}[/color]\n"
