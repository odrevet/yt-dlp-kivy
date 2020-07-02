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
from settings_json import settings_json

class RV(RecycleView):
    pass

class ActionBarMain(ActionBar):
   pass

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

class DownloaderApp(App):
   ydl_opts = ObjectProperty({})
   url = StringProperty()
   filetmpl = '%(title)s.%(ext)s'

   def get_output_dir(self):
      if platform == 'android':
         return os.getenv('EXTERNAL_STORAGE')
      return expanduser("~")

   def build_config(self, config):
      config.setdefaults('youtube-dl', {
      'quiet': False,
      'nowarning': False,
      'ignoreerrors': False,
      'call_home': False,
      'nocheckcertificate': False, 
      'prefer_insecure': platform == 'android',
      'outtmpl' : join(self.get_output_dir(), self.filetmpl),
      'savedir': self.get_output_dir()
      })

   def build_settings(self, settings):
      settings.add_json_panel('youtube-dl', self.config, data=settings_json)

   def on_config_change(self, config, section, key, value):
      if(key == 'savedir'):
         self.ydl_opts['outtmpl'] = join(value, self.filetmpl)
      else:
         self.ydl_opts[key] = value

   def build(self):
      root_folder = self.user_data_dir
      cache_folder = os.path.join(root_folder, 'cache')
      print(cache_folder)
      if platform == 'android':
         request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
      
      self.ydl_opts['quiet'] = self.config.get('youtube-dl', 'quiet')
      self.ydl_opts['nowarning'] = self.config.get('youtube-dl', 'nowarning')
      self.ydl_opts['ignoreerrors'] = self.config.get('youtube-dl', 'ignoreerrors')
      self.ydl_opts['call_home'] = self.config.get('youtube-dl', 'call_home')
      self.ydl_opts['nocheckcertificate'] = self.config.get('youtube-dl', 'nocheckcertificate')
      self.ydl_opts['prefer_insecure'] = self.config.get('youtube-dl', 'prefer_insecure')
      self.ydl_opts['outtmpl'] = join(self.config.get('youtube-dl', 'savedir'), self.filetmpl)

      self.use_kivy_settings = False
      return RootLayout()

if __name__ == '__main__':
   DownloaderApp().run()
