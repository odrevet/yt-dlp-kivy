import kivy
import youtube_dl
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.utils import platform

class DownloadLocationDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SettingsPopup(Popup):
   file_path = StringProperty("/sdcard")
   save = ObjectProperty(None)

   def show_download_location_dialog(self):
      content = DownloadLocationDialog(save=self.save, cancel=self.dismiss_popup)
      self._popup = Popup(title="Save file", content=content,
                          size_hint=(0.9, 0.9))
      self._popup.open()

   def get_path(self, path, _):
      self.file_path = path
      self.dismiss_popup()