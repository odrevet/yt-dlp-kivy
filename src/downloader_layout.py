from functools import partial
import uuid
from datetime import datetime
import time
from collections import OrderedDict

import yt_dlp

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from status import STATUS_INIT, STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS

from logger import YdlLogger
from downloaderThread import DownloaderThread
from format_select_popup import FormatSelectPopup


class DownloaderLayout(BoxLayout):
    popup = None  # info display popup
    downloads = OrderedDict()
    downloads = OrderedDict(sorted(downloads.items(), key=lambda x: x[1]["timestamp"]))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.refresh_rv, 1)

    def refresh_rv(self, dt):
        downloads_array = list(self.downloads.values())
        self.ids.rv.data = sorted(downloads_array, key=lambda x: x["dt"], reverse=True)
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
            "meta": {},
        }

        self.downloads[download_id]["log"] += f"download id {download_id}\n"
        self.downloads[download_id]["log"] += f"with options {app.ydl_opts}\n"
        self.downloads[download_id]["log"] += f"saving to  {app.ydl_opts['outtmpl']}\n"

        try:
            if not bool(app.meta):
                display_format_popup = app.config.getboolean(
                    "general", "display_formats_popup"
                )
                display_format_popup = False  # WIP

                if display_format_popup:
                    with yt_dlp.YoutubeDL(app.ydl_opts) as ydl:
                        app.meta = ydl.sanitize_info(
                            ydl.extract_info(app.url, download=False)
                        )
                        self.popup = FormatSelectPopup(app.meta)
                        callback = partial(
                            self.on_format_select_popup_dismiss,
                            app.url,
                            app.ydl_opts,
                            download_id,
                        )
                        self.popup.bind(on_dismiss=callback)
                        self.popup.open()
                else:
                    self.start_download(app.url, app.ydl_opts, download_id)
        except Exception as e:
            self.downloads[download_id]["title"] = "Cannot retreive metadata"
            self.downloads[download_id]["log"] = str(e)
            self.downloads[download_id]["status"] = STATUS_ERROR

    def start_download(self, url, ydl_opts, download_id):
        self.downloads[download_id]["status"] = STATUS_IN_PROGRESS

        hook = self.make_hook(download_id)

        # Create a logger
        ydl_opts["logger"] = YdlLogger(self.downloads[download_id], download_id)
        ydl_opts["progress_hooks"] = [hook]

        # Run in a thread so the UI do not freeze when download
        t = DownloaderThread(url, ydl_opts, self.downloads[download_id])
        t.start()

    def make_hook(self, download_id):
        def hook(d):
            if d["status"] == "downloading":
                if "total_bytes" in d:
                    percent = d["downloaded_bytes"] / d["total_bytes"] * 100
                elif "total_bytes_estimate" in d:
                    percent = d["downloaded_bytes"] / d["total_bytes_estimate"] * 100
                else:
                    percent = 0.0
                self.downloads[download_id]["percent"] = percent

                self.downloads[download_id]["title"] = d["filename"]
                self.downloads[download_id]["ETA"] = time.strftime(
                    "%H:%M:%S", time.gmtime(d["eta"])
                )
            elif d["status"] == "finished":
                self.downloads[download_id]["status"] = STATUS_DONE

        return hook
