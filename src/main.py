import os
import sys
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.utils import platform
from io import StringIO
from os.path import expanduser, join, dirname
from enum import Enum
import threading
import youtube_dl

class Status(Enum):
   PROCESSING = 1
   DONE = 2

class LogPopup(Popup):
   log = StringProperty()

   def __init__(self, log, **kwargs):
      super(LogPopup, self).__init__(**kwargs)
      self.log = log

class DownloadStatusBar(BoxLayout):
   url = StringProperty()
   status = StringProperty()
   log = ''

   def append_log(self, text):
      self.log = self.log + text

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

   def run(self):
      self.download_status_bar.set_status(Status.PROCESSING)
      self.download_status_bar.append_log('Start of `' + self.name + '`\n')

      #Redirect ytdl stdout to a string FIXME android: redirect output somehow prevent downloads
      if platform != 'android':
         sys_stdout = sys.stdout
         str_stdout = StringIO()
         sys.stdout = str_stdout

      try:
         youtube_dl.main(self.ytdl_args)
      except SystemExit:    #ignore ytdl calls to sys.exit()
         pass
      except Exception:     #ignore exception 'str' object has no attribute 'write'
         pass

      if platform != 'android':
         #redirect back stedout to system stdout
         sys.stdout = sys_stdout
         log = str_stdout.getvalue()    #TODO: get output every n seconds instead of waiting end of youtube_dl.main
         self.download_status_bar.append_log(log)

      self.download_status_bar.append_log('End of `' + self.name + '`\n')
      self.download_status_bar.set_status(Status.DONE)

class DownloaderLayout(BoxLayout):
   def on_press_button_download(self, url, output_template):
      #Add UI status bar for this download
      download_status_bar = DownloadStatusBar()
      download_status_bar.url = url
      self.ids.downloads_status_bar_layout.add_widget(download_status_bar, index=len(self.ids.downloads_status_bar_layout.children))

      ytdl_args = []    #arguments to pass to youtube-dl

      #Plateforme specific arguments
      if platform == 'android':
         ytdl_args.extend(('--no-check-certificate', '--prefer-insecure'))
      elif platform == 'linux':
         ytdl_args.append('--no-warnings')

      ytdl_args.extend(('-o', output_template, url))    #common arguments

      t = DownloaderThread(url, ytdl_args, download_status_bar)    #Run youtube-dl in a thread
      t.start()

class DownloaderApp(App):
    output_dir = ''
    output_file = ''
    output_template = ''

    def get_output_dir(self):
       if platform == 'android':
          return os.getenv('EXTERNAL_STORAGE')
       elif platform == 'linux':
          return expanduser("~")

       return self.user_data_dir

    def build(self):
        self.output_dir = self.get_output_dir()
        self.output_file = '%(title)s.%(ext)s'
        self.output_template = os.path.join(self.output_dir, self.output_file)
        return DownloaderLayout()

if __name__ == '__main__':
   DownloaderApp().run()    #TODO android: continue to download video when app is unfocused
