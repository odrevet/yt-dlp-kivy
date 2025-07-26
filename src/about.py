import sys
import pkg_resources
import webbrowser
from subprocess import check_output, CalledProcessError, TimeoutExpired
import os

import yt_dlp
import yt_dlp.utils as utils

import kivy
from kivy.utils import platform
from kivy.uix.popup import Popup

from _version import __version__

class AboutPopup(Popup):
    def __init__(self, **kwargs):
        super(AboutPopup, self).__init__(**kwargs)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_android = self.test_ytdlp_ffmpeg_compatibility()
        
        self.ids.about_label.text = f"""[ref=https://github.com/odrevet/yt-dlp-kivy][b]Yt_dlp Kivy[/b][/ref] on {platform}
2018 - 2025 Olivier Drevet [b]ffmpeg test version in {script_dir}[/b]
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
{ffmpeg_android}
"""

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

    # ytdlp is using Popen to run commands
    # https://github.com/yt-dlp/yt-dlp/blob/30302df22b7b431ce920e0f7298cd10be9989967/yt_dlp/postprocessor/ffmpeg.py#L362
    def test_ytdlp_ffmpeg_android(self):
        from android.storage import app_storage_path
        cache_dir = os.path.join(app_storage_path(), 'cache')
        ffmpeg_path = os.path.join(cache_dir, 'ffmpeg')

        if not os.path.exists(ffmpeg_path):
            return "ffmpeg not found in cache"

        try:
            import yt_dlp.utils as utils

            # This is similar to what yt-dlp does internally
            # https://github.com/yt-dlp/yt-dlp/blob/30302df22b7b431ce920e0f7298cd10be9989967/yt_dlp/utils/_utils.py#L2156C1-L2167C18
            version_output = utils._get_exe_version_output(ffmpeg_path, ['-version'])

            if version_output:
                return f"yt-dlp can call ffmpeg: {version_output.split()[0:3]}"
            elif version_output is False:
                return "yt-dlp failed to execute ffmpeg (OSError)"
            else:
                return "yt-dlp ffmpeg returned non-zero exit code"

        except Exception as e:
            return f"Error testing yt-dlp compatibility: {e}"
