import os
import sys
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.utils import platform
from kivy.clock import Clock
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

class LogPopup(Popup):
   log = StringProperty()

   def __init__(self, log, **kwargs):
      super(LogPopup, self).__init__(**kwargs)
      self.log = log

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

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
   def __init__(self, name, ytdl_args, download_status_bar):
       threading.Thread.__init__(self)
       self.name = name
       self.ytdl_args = ytdl_args
       self.download_status_bar = download_status_bar


   def my_callback(self, strio_stdout, *largs):
      self.download_status_bar.log = strio_stdout.getvalue()

   def run(self):
      self.download_status_bar.set_status(Status.PROCESSING)

      # to show ytdl output in the UI, redirect stdout to a string
      sys_stdout = sys.stdout
      strio_stdout = StringIO()
      sys.stdout = strio_stdout

      Clock.schedule_interval(partial(self.my_callback, strio_stdout), 0.5)

      try:
         youtube_dl.main(self.ytdl_args)
      except SystemExit:
         print('System Exit...')
         pass
      except Exception as inst:
         print(inst)
         pass

      # redirect back stdout to system stdout
      sys.stdout = sys_stdout

      self.download_status_bar.set_status(Status.DONE)

class DownloaderLayout(BoxLayout):
   #output = primary_external_storage_path()
   file_path = StringProperty("/sdcard")

   def dismiss_popup(self):
      self._popup.dismiss()

   def show_save(self):
      content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
      self._popup = Popup(title="Save file", content=content,
                          size_hint=(0.9, 0.9))
      self._popup.open()

   def save(self, path, filename):
      self.file_path = os.path.join(path, filename)
      self.dismiss_popup()

   def on_press_button_download(self, url, output):
      if platform == 'android':
         request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                              Permission.READ_EXTERNAL_STORAGE])

      #Add UI status bar for this download
      download_status_bar = DownloadStatusBar()
      download_status_bar.url = url
      self.ids.downloads_status_bar_layout.add_widget(download_status_bar,
                                                      index=len(self.ids.downloads_status_bar_layout.children))

      # arguments to pass to youtube-dl
      ytdl_args = ['-o', output, url]

      #Plateforme specific arguments
      if platform == 'android':
         ytdl_args.extend(('--no-check-certificate', '--prefer-insecure'))

      t = DownloaderThread(url, ytdl_args, download_status_bar)    # run youtube-dl in a thread
      t.start()

class DownloaderApp(App):
   output_dir = ''
   output_file = ''
   output = ''

   def get_output_dir(self):
      if platform == 'android':
         return os.getenv('EXTERNAL_STORAGE')
      elif platform == 'linux':
         return expanduser("~")

      return self.user_data_dir

   def build(self):
      self.output_dir = self.get_output_dir()
      self.output_file = '%(title)s.%(ext)s'
      self.output = os.path.join(self.output_dir, self.output_file)
      return DownloaderLayout()

if __name__ == '__main__':
   DownloaderApp().run()    # TODO: under android, continue to download video when app is unfocused
