import sys

import kivy
import youtube_dl
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
import pkg_resources

class AboutPopup(Popup):
   about_text = StringProperty(f'''[b]Youtube-Dl Kivy[/b] 
Version 0.0.1 - 2018 - 2020 Olivier Drevet 
Released Under the GPL-V3 License

[b]Youtube-dl[/b] 
Version {pkg_resources.get_distribution('Youtube-dl').version} 
Unlicense License

[b]Kivy[/b]
Version {kivy.__version__}
MIT License

[b]Python[/b] 
Version {sys.version}

[b]Icons[/b]
by Freepik from www.flaticon.com''')