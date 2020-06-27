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
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.uix.button import Button
import threading
import youtube_dl

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
    def debug(self, msg):
       print('DEBUG: ' + msg);
       pass

    def warning(self, msg):
       print('WARNING: ' + msg);
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

class DownloaderThread(threading.Thread):
   def __init__(self, url, ydl_opts, rv):
       threading.Thread.__init__(self)
       self.url = url
       self.ydl_opts = ydl_opts
       self.datum = rv.data[-1]
       self.rv = rv

   def callback_refresh_log(self, strio_stdout, *largs):
      self.datum['log'] = strio_stdout.getvalue()
      self.rv.refresh_from_data()

   def run(self):
      self.datum['status'] = 'Processing'

      # to show ytdl output in the UI, redirect stdout to a string
      sys_stdout = sys.stdout
      strio_stdout = StringIO()
      sys.stdout = strio_stdout

      Clock.schedule_interval(partial(self.callback_refresh_log, strio_stdout), 0.25)

      try:
         with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            download_retcode = ydl.download([self.url])
            self.datum['status'] = f'Done ({download_retcode})'
            print(f'Finished with retcode {download_retcode}')
            sys.stdout = sys_stdout
            self.rv.refresh_from_data()
      except SystemExit:
         print('System Exit...')
         pass
      except Exception as inst:
         print(inst)
         tb = traceback.format_exc()
         print(tb)
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
      t = DownloaderThread(url, ydl_opts, self.ids.rv)
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
