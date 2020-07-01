from __future__ import unicode_literals

import os
import sys
import threading
import traceback
from functools import partial
from io import StringIO
from os.path import dirname, expanduser, join

import kivy
import youtube_dl

class DownloaderThread(threading.Thread):
   def __init__(self, url, ydl_opts):
       threading.Thread.__init__(self)
       self.url = url
       self.ydl_opts = ydl_opts
       self.logger = ydl_opts['logger']

   def run(self):
      try:
         with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            download_retcode = ydl.download([self.url])
            self.logger.debug(f'Finished with retcode {download_retcode}')
      except SystemExit:
         self.logger.debug('System Exit')
         pass
      except Exception as inst:
         self.logger.error(inst)
         self.logger.error(traceback.format_exc())
         pass
