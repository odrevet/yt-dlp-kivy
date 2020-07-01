import os
import sys
import threading
import traceback
from os.path import expanduser, join

import kivy
import youtube_dl
from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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

from downloaderThread import DownloaderThread
from about import AboutPopup
from logger import YdlLogger, ydl_progress_hook

class RV(RecycleView):
    pass

class ActionBarMain(ActionBar):
   def on_press_about_button(self):
      AboutPopup().open()

class LogPopup(Popup):
   log = StringProperty()
   index = NumericProperty()

   def __init__(self, log, index, **kwargs):
      super(LogPopup, self).__init__(**kwargs)
      self.log = log
      self.index = index

class DownloadStatusBar(BoxLayout):
   url = StringProperty()
   status = StringProperty()
   log = StringProperty()
   index = NumericProperty()
   popup = None

   def on_release_show_log_button(self):
      self.popup = LogPopup(self.log, self.index)
      self.popup.open()

   def on_log(self, instance, value):
      if(self.popup is not None and instance.index == self.popup.index):
         self.popup.log = value

class DownloaderLayout(BoxLayout):
   def on_press_button_download(self, url, ydl_opts):
      if platform == 'android':
         #TODO permanently accept instead of asking each time the app is run
         request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

      # Add UI status bar for this download
      self.ids.rv.data.append({'url': url, 'index': len(self.ids.rv.data) - 1, 'log': '', 'status': 'processing'})

      # Create a logger and merge it in the ydl options
      logger = YdlLogger(self.ids.rv, len(self.ids.rv.data) - 1)
      ydl_opts = {**ydl_opts, **{'logger': logger,
                                 'progress_hooks': [ydl_progress_hook]}}

      # Run youtube-dl in a thread so the UI do not freeze
      t = DownloaderThread(url, ydl_opts, self.ids.rv.data[-1])
      t.start()

class RootLayout(BoxLayout):
   pass

def get_output_dir():
   if platform == 'android':
      return os.getenv('EXTERNAL_STORAGE')
   return expanduser("~")

class DownloaderApp(App):
   ydl_opts = ObjectProperty({})
   url = StringProperty()

   def set_param(self, id, value):
      self.ydl_opts[id]=value

   def build_config(self, config):
      config.setdefaults('youtube-dl', {
      'verbose': False,
      'quiet': False,
      'nowarning': False,
      'ignoreerrors': False,
      'call_home': False,
      'nocheckcertificate': False, 
      'prefer_insecure': platform == 'android',
      'outtmpl' : join(get_output_dir(), '%(title)s.%(ext)s')})

   def build_settings(self, settings):
      settings.add_json_panel('youtube-dl', self.config, 'src/settings.json')

   def on_config_change(self, config, section, key, value):
      self.ydl_opts[key] = value

   def build(self):
      self.config.items('youtube-dl')
      self.use_kivy_settings = False
      return RootLayout()

if __name__ == '__main__':
   DownloaderApp().run()
