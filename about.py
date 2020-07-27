import sys
import subprocess
import pkg_resources
import webbrowser
import youtube_dl
import kivy
from kivy.properties import StringProperty
from kivy.uix.popup import Popup


class AboutPopup(Popup):
    ffmpeg_output = ''

    def __init__(self, **kwargs):
        super(AboutPopup, self).__init__(**kwargs)

        try:
            self.ffmpeg_output = subprocess.check_output(['ffmpeg', "-version"])
        except OSError as e:
            if e.errno == errno.ENOENT:
                self.ffmpeg_output = 'ffmpeg was not found : ' + str(e)
            else:
                self.ffmpeg_output = 'Error while trying to get ffmpeg version: ' + str(e)

        self.ids.about_label.text = f'''[ref=https://github.com/odrevet/youtube-dl-kivy][b]Youtube-Dl Kivy[/b][/ref]
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
by Freepik from www.flaticon.com

[ref=https://ffmpeg.org/][b]ffmpeg[/b][/ref]
{self.ffmpeg_output}'''

    def on_ref_press(self, url):
        webbrowser.open(url)
