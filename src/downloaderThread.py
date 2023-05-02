import threading
import traceback

import yt_dlp

from status import STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS


class DownloaderThread(threading.Thread):
    def __init__(self, url, ydl_opts, meta):
        threading.Thread.__init__(self)
        self.url = url
        self.ydl_opts = ydl_opts
        self.logger = ydl_opts["logger"]
        self.meta = meta

    def run(self):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                retcode = ydl.download([self.url])
                self.logger.debug(f"Finished with retcode {retcode}")
                self.meta["status"] = STATUS_DONE if retcode == 0 else STATUS_ERROR
        except SystemExit:
            self.logger.debug("System Exit")
            self.meta["status"] = STATUS_ERROR
            pass
        except Exception as inst:
            self.logger.error(inst)
            self.logger.error(traceback.format_exc())
            self.meta["status"] = STATUS_ERROR
            pass
