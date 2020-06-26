from __future__ import unicode_literals
import os
import sys
import kivy
import traceback
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.actionbar import ActionBar
from io import StringIO
from os.path import expanduser, join, dirname
from enum import Enum
from functools import partial
import threading
import youtube_dl

if platform == 'android':
   from android.storage import primary_external_storage_path
   from android.permissions import request_permissions, Permission

class Status(Enum):
   PROCESSING = 1
   DONE = 2

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
   pass

class LogPopup(Popup):
   log = StringProperty()

   def __init__(self, log, **kwargs):
      super(LogPopup, self).__init__(**kwargs)
      self.log = log

class YdlLogger(object):
    def debug(self, msg):
       print('DEBUG: ' + msg);
       pass

    def warning(self, msg):
       print('DEBUG: ' + msg);
       pass

    def error(self, msg):
       print('ERROR: ' + msg)


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

   def set_status(self, status):
      if status == Status.PROCESSING:
         self.status = 'Processing'
      elif status == Status.DONE:
         self.status = 'Done'

class DownloaderThread (threading.Thread):
   def __init__(self, url, ydl_opts, download_status_bar):
       threading.Thread.__init__(self)
       self.url = url
       self.ydl_opts = ydl_opts
       self.download_status_bar = download_status_bar


   def callback_refresh_log(self, strio_stdout, *largs):
      self.download_status_bar.log = strio_stdout.getvalue()

   def run(self):
      self.download_status_bar.set_status(Status.PROCESSING)

      # to show ytdl output in the UI, redirect stdout to a string
      sys_stdout = sys.stdout
      strio_stdout = StringIO()
      sys.stdout = strio_stdout

      Clock.schedule_interval(partial(self.callback_refresh_log, strio_stdout), 0.5)

      download_retcode = None

      try:
         with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            download_retcode = ydl.download([self.url])
            print(f'Finished with retcode {download_retcode}')
      except SystemExit:
         print('System Exit...')
         pass
      except Exception as inst:
         print(inst)
         tb = traceback.format_exc()
         print(tb)
         pass

      # redirect back stdout to system stdout
      sys.stdout = sys_stdout

      self.download_status_bar.set_status(Status.DONE)

class DownloaderLayout(BoxLayout):
   def dismiss_popup(self):
      self._popup.dismiss()

   def on_press_button_download(self, url, outtmpl):
      if platform == 'android':
         #TODO permanently accept instead of asking each time the app is run
         request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                              Permission.READ_EXTERNAL_STORAGE])

      #Add UI status bar for this download
      download_status_bar = DownloadStatusBar()
      download_status_bar.url = url
      self.ids.downloads_status_bar_layout.add_widget(download_status_bar,
                                                      index=len(self.ids.downloads_status_bar_layout.children))

      ydl_opts = {'outtmpl':outtmpl,
                   'ignoreerrors':True,
                   'logger': YdlLogger(),
                   'progress_hooks': [ydl_progress_hook]}

      #Platform default arguments
      if platform == 'android':
         ydl_opts['nocheckcertificate'] = True
         ydl_opts['prefer_insecure'] = True
      elif platform == 'linux':
         ydl_opts['--no-warnings'] = True

      # Run youtube-dl in a thread so the UI do not freeze
      t = DownloaderThread(url, ydl_opts, download_status_bar)
      t.start()

class RootLayout(BoxLayout):
   pass

class DownloaderApp(App):
   output_dir = ''
   output_file = ''
   outtmpl = ''

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
