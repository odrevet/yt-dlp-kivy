import re


class YdlLogger(object):
    rv = None

    def __init__(self, rv, index):
        self.rv = rv
        self.index = index

    def debug(self, msg):
        m = re.search(
            r"^\[download\]\s+(\d+\.\d+)%\s+of\s+(\d+\.\d+\w+)\s+at\s+(\d+\.\d+\w+\/s)\s+ETA\s+(\d{2}:\d{2})$",
            msg,
        )

        if m is not None:
            self.rv.data[self.index]["percent"] = float(m.group(1))
            self.rv.data[self.index]["file_size"] = m.group(2)
            self.rv.data[self.index]["speed"] = m.group(3)
            self.rv.data[self.index]["ETA"] = m.group(4)
        else:
            self.rv.data[self.index]["log"] += f"{msg}\n"
            if msg.endswith("has already been downloaded"):
                self.rv.data[self.index]["percent"] = 100
                self.rv.data[self.index]["ETA"] = "Video has alderly been downloaded"

        self.rv.refresh_from_data()

    def warning(self, msg):
        self.rv.data[self.index]["log"] += f"[color=ffff00]{msg}[/color]\n"
        self.rv.refresh_from_data()

    def error(self, msg):
        self.rv.data[self.index]["log"] += f"[color=ff0000]{msg}[/color]\n"
        self.rv.refresh_from_data()
