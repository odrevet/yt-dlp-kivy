import sys

import kivy
import youtube_dl
from kivy.properties import StringProperty
from kivy.uix.popup import Popup

class AboutPopup(Popup):
   about_text = StringProperty(f'''Youtube-Dl Kivy Version 0.0.1 - 2018 - 2020 Olivier Drevet
Kivy Version {kivy. __version__}
Python Version {sys.version} {sys.version_info}''')