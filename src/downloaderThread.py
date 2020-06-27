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
from kivy.clock import Clock


class DownloaderThread(threading.Thread):
   def __init__(self, url, ydl_opts, rv):
       threading.Thread.__init__(self)
       self.url = url
       self.ydl_opts = ydl_opts
       self.datum = rv.data[-1]
       self.rv = rv
       self.logger = ydl_opts['logger']

   def callback_refresh_log(self, *largs):
      self.datum['log'] = self.logger.log
      self.rv.refresh_from_data()

   def run(self):
      self.datum['status'] = 'Processing'

      Clock.schedule_interval(partial(self.callback_refresh_log), 0.25)

      try:
         with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            download_retcode = ydl.download([self.url])
            self.datum['status'] = f'Done ({download_retcode})'
            print(f'Finished with retcode {download_retcode}')
            self.rv.refresh_from_data()
      except SystemExit:
         self.logger.debug('System Exit')
         pass
      except Exception as inst:
         self.logger.error(inst)
         self.logger.error(traceback.format_exc())
         pass
