from functools import partial
import uuid
from datetime import datetime
import time

import yt_dlp

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from status import STATUS_INIT, STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS

from logger import YdlLogger
from downloaderThread import DownloaderThread
from format_select_popup import FormatSelectPopup

from download_status_bar import DownloadStatusBar

class DownloaderLayout(BoxLayout):
    popup = None  # info display popup
    downloads = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.refresh_downloads, 1)
    
    def refresh_downloads(self, dt):
        """Refresh the downloads display - now only updates existing widgets"""
        downloads_layout = self.ids.downloads_layout
        
        # Update existing widgets instead of recreating them
        current_download_ids = set()
        for download_id, download_data in self.downloads.items():
            current_download_ids.add(download_id)
            
            # Find existing widget or create new one
            existing_widget = None
            for widget in downloads_layout.children:
                if hasattr(widget, 'id') and widget.id == download_id:
                    existing_widget = widget
                    break
            print(download_data)
            if existing_widget:
                # Update existing widget
                existing_widget.update_from_data(download_data)
            else:
                # Create new widget
                download_widget = DownloadStatusBar()
                download_widget.update_from_data(download_data)
                downloads_layout.add_widget(download_widget)
        
        # Remove widgets for downloads that no longer exist
        widgets_to_remove = []
        for widget in downloads_layout.children:
            if hasattr(widget, 'id') and widget.id not in current_download_ids:
                widgets_to_remove.append(widget)
        
        for widget in widgets_to_remove:
            downloads_layout.remove_widget(widget)

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
            "filename": "",
            "status": STATUS_INIT,
            "meta": {},
            "ydl_opts" : {}
        }

        self.downloads[download_id]["log"] += f"download id {download_id}\n"
        self.downloads[download_id]["log"] += f"with options {app.ydl_opts}\n"
        self.downloads[download_id]["log"] += f"saving to {app.ydl_opts['savedir']}\n"

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
            self.downloads[download_id]["log"] += str(e)
            self.downloads[download_id]["status"] = STATUS_ERROR

    def start_download(self, url, ydl_opts, download_id):
        # Update the status
        self.downloads[download_id]["status"] = STATUS_IN_PROGRESS

        # Copy options then create the logger and progress hook
        self.downloads[download_id]["ydl_opts"] = ydl_opts.copy()
        self.downloads[download_id]["ydl_opts"]["logger"] = YdlLogger(self.downloads[download_id], download_id)
        self.downloads[download_id]["ydl_opts"]["progress_hooks"] = [self.make_hook(download_id)]

        # Run in a thread so the UI do not freeze when download
        t = DownloaderThread(url, self.downloads[download_id])
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
                self.downloads[download_id]["filename"] = d["filename"]
                self.downloads[download_id]["ETA"] = time.strftime(
                    "%H:%M:%S", time.gmtime(d["eta"])
                )
                self.downloads[download_id]["status"] = STATUS_IN_PROGRESS
            elif d["status"] == "finished":
                self.downloads[download_id]["status"] = STATUS_DONE
            elif d["status"] == "error":
                self.downloads[download_id]["status"] = STATUS_ERROR
                self.downloads[download_id]["percent"] = 0.0

        return hook
