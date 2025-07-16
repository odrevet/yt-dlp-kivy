import os
import sys
import threading
from functools import partial
from os.path import expanduser, join
import uuid
from datetime import datetime
import time

import yt_dlp

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import DictProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

from about import AboutPopup
from downloaderThread import DownloaderThread
from logger import YdlLogger
from settings_json import settings_json
from status import STATUS_INIT, STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS

if platform == "android":
    from android.storage import primary_external_storage_path
    from android.permissions import check_permission, request_permissions, Permission
    from android.storage import app_storage_path

    cache_dir = os.path.join(app_storage_path(), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    os.environ['XDG_CACHE_HOME'] = cache_dir

class RV(RecycleView):
    pass


class ActionBarMain(ActionBar):
    pass


class LogPopup(Popup):
    log = StringProperty()
    id = ObjectProperty()

    def __init__(self, log, index, **kwargs):
        super(LogPopup, self).__init__(**kwargs)
        self.log = "\n".join(log.split("\n")[-300:]) # truncat log
        self.id = id

class FormatSelectPopup(Popup):
    meta = {}
    selected_format_id = []

    def __init__(self, meta, **kwargs):
        super(FormatSelectPopup, self).__init__(**kwargs)
        self.selected_format_id.clear()
        
        if not meta or "formats" not in meta:
            print("Error: No formats found in metadata")
            grid = self.ids.layout
            grid.add_widget(Label(text="No formats found"))
            return
        else:
            formats_sorted = sorted(meta["formats"], key=lambda k: k["format"])
            for format in formats_sorted:
                grid = self.ids.layout
                grid.add_widget(Label(text=format["format"] + " " + format["ext"]))
                checkbox = CheckBox(active=False, size_hint_x=None, width=100)
                callback = partial(self.on_checkbox_active, format["format_id"])
                checkbox.bind(active=callback)
                grid.add_widget(checkbox)

    def on_checkbox_active(self, format_id, instance, value):
        if value:
            self.selected_format_id.append(format_id)
        else:
            self.selected_format_id.remove(format_id)


class DownloadStatusBar(BoxLayout):
    url = StringProperty("")
    status = NumericProperty(STATUS_IN_PROGRESS)
    log = StringProperty("")
    id = ObjectProperty()
    status_icon = StringProperty("img/loader.png")
    title = StringProperty("")
    percent = NumericProperty(0)
    ETA = StringProperty("")
    speed = StringProperty("")
    file_size = StringProperty("")
    popup = None

    def on_release_show_log_button(self):
        self.popup = LogPopup(self.log, self.id)
        self.popup.open()

    def on_status(self, instance, value):
        if value == STATUS_IN_PROGRESS:
            self.status_icon = "img/loader.png"
        elif value == STATUS_DONE:
            self.status_icon = "img/correct.png"
        elif value == STATUS_ERROR:
            self.status_icon = "img/cancel.png"

    def on_log(self, instance, value):
        if self.popup is not None and instance.id == self.popup.id:
            self.popup.log = value


class DownloaderLayout(BoxLayout):
    popup = None  # info display popup
    downloads = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.refresh_rv, 1)

    def refresh_rv(self, dt):
        downloads_array = list(self.downloads.values())
        self.ids.rv.data = sorted(downloads_array, key=lambda x: x['dt'], reverse=True)
        self.ids.rv.refresh_from_data()

    def on_format_select_popup_dismiss(self, url, ydl_opts, download_id, instance):
        if instance.selected_format_id:
            self.start_download(
                url,
                {**ydl_opts, **{"format": ",".join(instance.selected_format_id)}},
                download_id,
            )

    def on_press_button_download(self):
        app = App.get_running_app()

        download_id = uuid.uuid4()

        # Add UI status bar for this download
        self.downloads[download_id] = {
            "id": download_id,
            "dt": datetime.now(),
            "url": app.url,
            "log": "",
            "title": "",
            "status": STATUS_INIT,
            "meta": {}
            }
        
        try:
            if not bool(app.meta):
                with yt_dlp.YoutubeDL(app.ydl_opts) as ydl:
                    app.meta = ydl.sanitize_info(ydl.extract_info(app.url, download=False))

                format_method = app.config.get("general", "method")
                if format_method == "Ask":
                    self.popup = FormatSelectPopup(app.meta)
                    callback = partial(
                        self.on_format_select_popup_dismiss, app.url, app.ydl_opts, download_id
                    )
                    self.popup.bind(on_dismiss=callback)
                    self.popup.open()
                else:
                    self.start_download(app.url, app.ydl_opts, download_id)
        except Exception as e:
            self.downloads[download_id]["meta"]["title"] = "Cannot retreive metadata"
            self.downloads[download_id]["log"] = str(e)
            self.downloads[download_id]["status"] = STATUS_ERROR
            

    def start_download(self, url, ydl_opts, download_id):
        self.downloads[download_id]["status"] = STATUS_IN_PROGRESS

        hook = self.make_hook(download_id)
            
        # Create a logger
        ydl_opts["logger"] = YdlLogger(self.downloads[download_id])
        ydl_opts["progress_hooks"] = [hook]

        # Run in a thread so the UI do not freeze when download
        t = DownloaderThread(url, ydl_opts, self.downloads[download_id])
        t.start()

    def make_hook(self, download_id):
        def hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                elif 'total_bytes_estimate' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                else:
                    percent = 0.0
                self.downloads[download_id]["percent"] = percent

                self.downloads[download_id]["title"] = d['filename']
                self.downloads[download_id]["ETA"] = time.strftime('%H:%M:%S', time.gmtime(d['eta']))

                if d['status'] == 'finished':
                    self.downloads[download_id]["status"] = STATUS_FINISHED
                    
        return hook


class RootLayout(Label):
    pass


class StatusIcon(Label):
    status = NumericProperty(1)


class DownloaderApp(App):
    meta = {}
    ydl_opts = {'no_color': True}
    url = StringProperty()

    def get_output_dir(self):
        if platform == "android":
            return os.getenv("EXTERNAL_STORAGE") + "/Download"
        return expanduser("~")

    def build_config(self, config):
        config.setdefaults(
            "general",
            {
                "method": "Preset",
                "preset": "best",
                "ignoreerrors": False,
                "filetmpl": "%(title)s_%(format)s.%(ext)s",
                "savedir": self.get_output_dir(),
            })

        config.setdefaults(
            "verbosity",
            {
                "quiet": False,
                "nowarning": False,
            })

        config.setdefaults(
            "workarounds",
            {
                "nocheckcertificate": False,
                "prefer_insecure": platform == "android",
            })

    def build_settings(self, settings):
        settings.add_json_panel("Settings", self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if key == "savedir":
            self.ydl_opts["outtmpl"] = join(
                value, self.config.get("general", "filetmpl")
            )
        elif key == "filetmpl":
            self.ydl_opts["outtmpl"] = join(
                self.config.get("general", "savedir"), value
            )
        elif key == "preset" or (key == "method" and value == "Preset"):
            self.ydl_opts["format"] = self.config.get("general", "preset")
        elif key == "method" and value == "Ask":
            self.ydl_opts.pop("format", None)
        else:
            self.ydl_opts[key] = value

    def build(self):
        if platform == "android" and not check_permission(
                "android.permission.WRITE_EXTERNAL_STORAGE"
        ):
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

        # general
        self.ydl_opts["ignoreerrors"] = self.config.get("general", "ignoreerrors")

        self.ydl_opts["outtmpl"] = join(
            self.config.get("general", "savedir"),
            self.config.get("general", "filetmpl"),
        )

        if self.config.get("general", "method") == "Preset":
            self.ydl_opts["format"] = self.config.get("general", "preset")

        # workarounds
        self.ydl_opts["nocheckcertificate"] = self.config.get("workarounds", "nocheckcertificate")
        self.ydl_opts["prefer_insecure"] = self.config.get("workarounds", "prefer_insecure")

        # # verbosity
        self.ydl_opts["quiet"] = self.config.get("verbosity", "quiet")
        self.ydl_opts["nowarning"] = self.config.get("verbosity", "nowarning")

        self.use_kivy_settings = False
        return RootLayout()


if __name__ == "__main__":
    DownloaderApp().run()
