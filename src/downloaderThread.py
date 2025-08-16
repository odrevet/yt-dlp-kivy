import threading
import traceback

import yt_dlp

from status import STATUS_DONE, STATUS_ERROR


class DownloaderThread(threading.Thread):
    def __init__(self, url, download):
        threading.Thread.__init__(self)
        self.url = url
        self.ydl_opts = download["ydl_opts"]
        self.logger = download["ydl_opts"]["logger"]
        self.download = download

    def run(self):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                retcode = ydl.download([self.url])
                self.logger.debug(f"Finished with retcode {retcode}")
                self.download["status"] = STATUS_DONE if retcode == 0 else STATUS_ERROR
        except SystemExit:
            self.logger.debug("System Exit")
            self.download["status"] = STATUS_ERROR
        except Exception as inst:
            self.logger.error(inst)
            self.logger.error(traceback.format_exc())
            self.download["status"] = STATUS_ERROR
