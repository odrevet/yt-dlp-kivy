from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    ObjectProperty,
)
from kivy.uix.popup import Popup


class LogPopup(Popup):
    log = StringProperty()
    download_id = ObjectProperty()
    refresh_event = None

    def __init__(self, log, download_id, downloads_dict, **kwargs):
        super(LogPopup, self).__init__(**kwargs)
        self.log = "\n".join(log.split("\n")[-300:])  # truncate log
        self.download_id = download_id
        self.downloads_dict = downloads_dict

        # Schedule periodic refresh
        self.refresh_event = Clock.schedule_interval(self.refresh_log, 1.0)

    def refresh_log(self, dt):
        """Refresh log content from the downloads dictionary"""
        if self.download_id in self.downloads_dict:
            new_log = self.downloads_dict[self.download_id]["log"]
            # Truncate to last 300 lines to prevent memory issues
            self.log = "\n".join(new_log.split("\n")[-300:])

    def on_dismiss(self):
        """Clean up the refresh event when popup is closed"""
        if self.refresh_event:
            self.refresh_event.cancel()
        super().on_dismiss()
