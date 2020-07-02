import sys

import kivy
import youtube_dl
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
import pkg_resources

class AboutPopup(Popup):
   about_text = StringProperty(f'''*Youtube-Dl Kivy Version 0.0.1 - 2018 - 2020 Olivier Drevet 
Released Under the GPL-V3 License

* Youtube-dl version {pkg_resources.get_distribution('Youtube-dl').version} Unlicense License

* Kivy Framework version {kivy.__version__} MIT License

* Python language version {sys.version}''')