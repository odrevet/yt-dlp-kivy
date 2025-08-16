from kivy.app import App
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty,
)
from kivy.uix.boxlayout import BoxLayout

from status import STATUS_INIT, STATUS_DONE, STATUS_IN_PROGRESS, STATUS_ERROR
from log_popup import LogPopup


class DownloadStatusBar(BoxLayout):
    url = StringProperty("")
    status = NumericProperty(STATUS_INIT)
    log = StringProperty("")
    id = ObjectProperty()
    title = StringProperty("")
    status_icon = StringProperty("img/loader.png")
    percent = NumericProperty(0)
    ETA = StringProperty("")
    speed = StringProperty("")
    file_size = StringProperty("")
    popup = None

    def on_release_show_log_button(self):
        app = App.get_running_app()
        downloader_layout = app.root.ids.main_layout

        self.popup = LogPopup(self.log, self.id, downloader_layout.downloads)
        self.popup.open()

    def on_status(self, instance, value):
        if value == STATUS_INIT:
            self.title = "Init"
            self.status_icon = "img/loader.png"
        elif value == STATUS_DONE:
            self.title = "Done " + App.get_running_app().root.ids.main_layout.downloads[self.id]["filename"]
            self.status_icon = "img/correct.png"
        elif value == STATUS_IN_PROGRESS:
            self.title = "Downloading " + App.get_running_app().root.ids.main_layout.downloads[self.id]["filename"]
            self.status_icon = "img/loader.png"
        elif value == STATUS_ERROR:
            self.title = "Error"
            self.status_icon = "img/cancel.png"