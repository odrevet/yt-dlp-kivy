import threading
import traceback

import youtube_dl

class DownloaderThread(threading.Thread):
   def __init__(self, url, ydl_opts, datum):
       threading.Thread.__init__(self)
       self.url = url
       self.ydl_opts = ydl_opts
       self.logger = ydl_opts['logger']
       self.datum = datum

   def run(self):
      try:
         with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            download_retcode = ydl.download([self.url])
            self.logger.debug(f'Finished with retcode {download_retcode}')
            self.datum['status'] = f'Done ({download_retcode})'
      except SystemExit:
         self.logger.debug('System Exit')
         self.datum['status'] = 'Done (exited)'
         pass
      except Exception as inst:
         self.logger.error(inst)
         self.logger.error(traceback.format_exc())
         self.datum['status'] = 'Done (error)'
         pass
