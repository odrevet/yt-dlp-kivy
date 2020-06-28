import kivy
import youtube_dl
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.utils import platform

if platform == 'android':
   from android.storage import primary_external_storage_path
   from android.permissions import request_permissions, Permission

class DownloadLocationDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    filename = ObjectProperty(None)

class SettingsPopup(Popup):
    path = StringProperty("/sdcard")

    def dismiss_popup(self):
      self._popup.dismiss()

    def show_download_location_dialog(self):
        if platform == 'android':
            #TODO permanently accept instead of asking each time the app is run
            request_permissions([Permission.READ_EXTERNAL_STORAGE])

        content = DownloadLocationDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
      self.path = path
      self.dismiss_popup()