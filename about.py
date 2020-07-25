import sys

import kivy
import youtube_dl
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
import pkg_resources
import webbrowser


class AboutPopup(Popup):
    about_text = StringProperty(f'''[ref=https://github.com/odrevet/youtube-dl-kivy][b]Youtube-Dl Kivy[/b][/ref] 
2020 Olivier Drevet
Version 0.2.1
Released Under the GPL-v3 License

[ref=https://youtube-dl.org/][b]Youtube-dl[/b][/ref] 
Version {pkg_resources.get_distribution('Youtube-dl').version} 
Unlicense License

[ref=https://kivy.org][b]Kivy[/b][/ref]
Version {kivy.__version__}
MIT License

[ref=https://www.python.org][b]Python[/b][/ref] 
Version {sys.version}

[ref=https://www.flaticon.com][b]Icons[/b][/ref]
by Freepik from www.flaticon.com''')

    def on_ref_press(self, url):
        webbrowser.open(url)
