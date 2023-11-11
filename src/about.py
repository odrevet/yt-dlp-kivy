import sys
from subprocess import check_output
import pkg_resources
import webbrowser
import yt_dlp
import kivy
from kivy.properties import StringProperty
from kivy.uix.popup import Popup


class AboutPopup(Popup):
    ffmpeg_output = ""

    def __init__(self, **kwargs):
        super(AboutPopup, self).__init__(**kwargs)

        try:
            self.ffmpeg_output = check_output("ffmpeg -version", shell=True)
        except Exception as e:
            self.ffmpeg_output = "ffmpeg not found"

        self.ids.about_label.text = f"""[ref=https://github.com/odrevet/yt-dlp-kivy][b]Yt_dlp Kivy[/b][/ref]
2023 Olivier Drevet
Version 0.3.3
Released Under the GPL-v3 License

[ref=https://github.com/yt-dlp/yt-dlp][b]yt-dlp[/b][/ref]
Version {pkg_resources.get_distribution('yt-dlp').version}
Unlicense License

[ref=https://kivy.org][b]Kivy[/b][/ref]
Version {kivy.__version__}
MIT License

[ref=https://www.python.org][b]Python[/b][/ref]
Version {sys.version}

[ref=https://heroicons.dev][b]Icons[/b][/ref]
by heroicons
MIT License

[ref=https://ffmpeg.org/][b]ffmpeg[/b][/ref]
{self.ffmpeg_output}"""

    def on_ref_press(self, url):
        webbrowser.open(url)
