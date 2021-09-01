import threading
import traceback

import youtube_dl

from status import STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS


class DownloaderThread(threading.Thread):
    def __init__(self, url, ydl_opts, datum):
        threading.Thread.__init__(self)
        self.url = url
        self.ydl_opts = ydl_opts
        self.logger = ydl_opts["logger"]
        self.datum = datum

    def run(self):
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                retcode = ydl.download([self.url])
                self.logger.debug(f"Finished with retcode {retcode}")
                self.datum["status"] = STATUS_DONE if retcode == 0 else STATUS_ERROR
        except SystemExit:
            self.logger.debug("System Exit")
            self.datum["status"] = STATUS_ERROR
            pass
        except Exception as inst:
            self.logger.error(inst)
            self.logger.error(traceback.format_exc())
            self.datum["status"] = STATUS_ERROR
            pass
