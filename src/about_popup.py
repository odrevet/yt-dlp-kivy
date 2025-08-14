import sys
import pkg_resources
import webbrowser
import sys
from subprocess import check_output, CalledProcessError, TimeoutExpired

import yt_dlp.utils as utils

import kivy
from kivy.utils import platform
from kivy.uix.popup import Popup

from _version import __version__

class AboutPopup(Popup):
    def __init__(self, **kwargs):
        super(AboutPopup, self).__init__(**kwargs)
        
        ffmpeg_location = self.get_ffmpeg_info()
        
        self.ids.about_label.text = f"""[ref=https://github.com/odrevet/yt-dlp-kivy][b]Yt_dlp Kivy[/b][/ref] on {platform}
2018 2025 Olivier Drevet
Version {__version__}
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
{ffmpeg_location}"""

    def on_ref_press(self, url):
        webbrowser.open(url)


    def get_ffmpeg_info(self):
        try:
            ffmpeg_exe = utils.check_executable('ffmpeg')
            if ffmpeg_exe:
                buffer = f"{ffmpeg_exe} found via yt-dlp"
                if platform in ('linux', 'win', 'macosx'):        
                    try:
                        output = check_output(f"{ffmpeg_exe} -version", shell=True, timeout=5)
                        buffer += "\n"
                        buffer += output.decode('utf-8').split('\n')[0]
                    except (CalledProcessError, TimeoutExpired, FileNotFoundError):
                        pass

                return buffer
        except:
            pass
            
        return "ffmpeg not found or not accessible"   
