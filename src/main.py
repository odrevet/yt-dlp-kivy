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
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

if platform == 'android':
   from android.storage import primary_external_storage_path
   from android.permissions import request_permissions, Permission

class RV(RecycleView):
    pass

class ActionBarMain(ActionBar):
   def on_press_settings_button(self):
      SettingsPopup().open()

   def on_press_about_button(self):
      AboutPopup().open()

class SettingsPopup(Popup):
   file_path = StringProperty("/sdcard")

   def get_path(self, path, _):
      self.file_path = path
      self.dismiss_popup()

class AboutPopup(Popup):
   about_text = StringProperty(f'''Youtube-Dl Kivy Version 0.0.1 - 2018 - 2020 Olivier Drevet
Kivy Version {kivy. __version__}
Python Version {sys.version} {sys.version_info}''')

class LogPopup(Popup):
   log = StringProperty()

   def __init__(self, log, **kwargs):
      super(LogPopup, self).__init__(**kwargs)
      self.log = log

class YdlLogger(object):
   log = ''

   def debug(self, msg):
      self.log += msg + "\n"

   def warning(self, msg):
      self.log += msg + "\n"

   def error(self, msg):
      self.log += msg + "\n"

def ydl_progress_hook(d):
   if d['status'] == 'finished':
      print('Done downloading')

class DownloadLocationDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def show_download_location_dialog(self):
       content = DownloadLocationDialog(save=self.save, cancel=self.dismiss_popup)
       self._popup = Popup(title="Save file", content=content,
                           size_hint=(0.9, 0.9))
       self._popup.open()


class DownloadStatusBar(BoxLayout):
   url = StringProperty()
   status = StringProperty()
   log = StringProperty()

   def on_release_show_log_button(self):
      popup = LogPopup(self.log)
      popup.open()

class DownloaderThread(threading.Thread):
   def __init__(self, url, ydl_opts, rv, logger):
       threading.Thread.__init__(self)
       self.url = url
       self.ydl_opts = ydl_opts
       self.datum = rv.data[-1]
       self.rv = rv
       self.logger = logger

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

class DownloaderLayout(BoxLayout):
   def dismiss_popup(self):
      self._popup.dismiss()

   def on_press_button_download(self, url, outtmpl):
      if platform == 'android':
         #TODO permanently accept instead of asking each time the app is run
         request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

      #Add UI status bar for this download
      data = self.ids.rv.data
      data.append({'url': url})

      logger = YdlLogger()

      ydl_opts = {'outtmpl':outtmpl,
                   'ignoreerrors':True,
                   'logger': logger,
                   'progress_hooks': [ydl_progress_hook]}

      #Platform default arguments
      if platform == 'android':
         ydl_opts['nocheckcertificate'] = True
         ydl_opts['prefer_insecure'] = True
      elif platform == 'linux':
         ydl_opts['--no-warnings'] = True

      # Run youtube-dl in a thread so the UI do not freeze
      t = DownloaderThread(url, ydl_opts, self.ids.rv, logger)
      t.start()

class RootLayout(BoxLayout):
   pass

class DownloaderApp(App):
   output_dir = ''
   output_file = ''
   outtmpl = ''

   url = StringProperty();

   def get_output_dir(self):
      if platform == 'android':
         return os.getenv('EXTERNAL_STORAGE')
      elif platform == 'linux':
         return expanduser("~")

      return self.user_data_dir

   def build(self):
      self.output_dir = self.get_output_dir()
      self.output_file = '%(title)s.%(ext)s'
      self.outtmpl = os.path.join(self.output_dir, self.output_file)
      return RootLayout()

if __name__ == '__main__':
   DownloaderApp().run()
