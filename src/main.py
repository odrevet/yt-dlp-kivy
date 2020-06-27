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

from settingsMenu import SettingsPopup
from downloaderThread import DownloaderThread
from about import AboutPopup
from logger import YdlLogger, ydl_progress_hook

class RV(RecycleView):
    pass

class ActionBarMain(ActionBar):
   def on_press_settings_button(self):
      SettingsPopup().open()

   def on_press_about_button(self):
      AboutPopup().open()

class LogPopup(Popup):
   log = StringProperty()

   def __init__(self, log, **kwargs):
      super(LogPopup, self).__init__(**kwargs)
      self.log = log

class DownloadStatusBar(BoxLayout):
   url = StringProperty()
   status = StringProperty()
   log = StringProperty()

   def on_release_show_log_button(self):
      popup = LogPopup(self.log)
      popup.open()

class DownloaderLayout(BoxLayout):
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
