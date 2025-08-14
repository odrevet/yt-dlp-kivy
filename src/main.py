import json
from collections import defaultdict
from os.path import expanduser, join

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (
    DictProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty,
)
from kivy.resources import resource_find
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
from kivy.uix.settings import Settings
from kivy.config import Config, ConfigParser

from status import STATUS_INIT, STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS

from downloader_layout import DownloaderLayout
from download_status_bar import DownloadStatusBar
from about_popup import AboutPopup

Builder.load_file("download_status_bar.kv")
Builder.load_file("log_popup.kv")

if platform == "android":
    from android.storage import primary_external_storage_path
    from android.permissions import check_permission, request_permissions, Permission
    from android.storage import app_storage_path

    cache_dir = os.path.join(app_storage_path(), "cache")
    os.makedirs(cache_dir, exist_ok=True)
    os.environ["XDG_CACHE_HOME"] = cache_dir


class DownloaderApp(App):
    meta = {}
    ydl_opts = {"no_color": True}
    url = StringProperty()
    section_options = defaultdict(lambda: defaultdict(list))
    use_kivy_settings = False

    def get_output_dir(self):
        if platform == "android":
            return os.getenv("EXTERNAL_STORAGE") + "/Download"
        return expanduser("~")

    def build(self):
        if platform == "android" and not check_permission(
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ):
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

        # Config
        config = ConfigParser()

        # remove red dots on right clic on desktop
        # also trigger on_release multiple time under android
        if platform in ("linux", "win", "macosx"):
            Config.set("input", "mouse", "mouse,multitouch_on_demand")

        # Find the resource file
        ini_file = resource_find("downloader.ini")
        if ini_file:
            config.read(ini_file)
            self.config = config
            self.settings_cls = Settings
            self.init_ydl_opts()
        else:
            print("------------------")
            print("INI file not found")

        savedir = self.config.get("general", "savedir")
        if not savedir:
            savedir = self.get_output_dir()

        self.ydl_opts["outtmpl"] = join(
            savedir,
            self.config.get("general", "filetmpl"),
        )

        return RootLayout()

    def build_settings(self, settings):
        settings_dir = "settings"
        settings_files = [
            ("General", f"{settings_dir}/general.json"),
            ("Network", f"{settings_dir}/network.json"),
            ("Geo-restriction", f"{settings_dir}/geo_restriction.json"),
            ("Video Selection", f"{settings_dir}/video_selection.json"),
            ("Download", f"{settings_dir}/download.json"),
            ("Filesystem", f"{settings_dir}/filesystem.json"),
            ("Format", f"{settings_dir}/video_format.json"),
            ("Subtitles", f"{settings_dir}/subtitle.json"),
            ("Authentication", f"{settings_dir}/authentification.json"),
            ("Post-Processing", f"{settings_dir}/post_processing.json"),
            ("SponsorBlock", f"{settings_dir}/sponsor_block.json"),
            ("Extractor", f"{settings_dir}/extractor.json"),
            ("Verbosity", f"{settings_dir}/verbosity.json"),
            ("Workarounds", f"{settings_dir}/workarounds.json"),
        ]

        # Build section_options from all JSONs
        section_options = defaultdict(lambda: defaultdict(list))
        for title, filename in settings_files:
            json_file = resource_find(filename)
            if json_file:
                with open(json_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        section = item.get("section")
                        typ = item.get("type")
                        key = item.get("key")
                        if section and typ and key:
                            section_options[section][typ].append(key)
                settings.add_json_panel(title, self.config, json_file)
            else:
                print(f"Warning: Settings file not found: {filename}")

        self.section_options = dict(section_options)

    def init_ydl_opts(self):
        for section, opts in self.section_options.items():
            for key_type, keys in opts.items():
                for key in keys:
                    if not self.config.get(section, key):
                        continue
                    if key_type == "bool":
                        self.ydl_opts[key] = self.config.getboolean(section, key)
                    elif key_type == "numeric":
                        self.ydl_opts[key] = self.config.getint(section, key)
                    elif (
                        key_type == "string"
                        or key_type == "path"
                        or key_type == "options"
                    ):
                        self.ydl_opts[key] = self.config.get(section, key)

    def on_config_change(self, config, section, key, value):
        if section not in self.section_options:
            return
        getters = {
            "bool": config.getboolean,
            "numeric": config.getint,
            "string": lambda s, k: value,
            "path": lambda s, k: value,
            "options": lambda s, k: value,
        }
        for typ, keys in self.section_options[section].items():
            if key in keys:
                self.ydl_opts[key] = getters[typ](section, key)
                break


class RV(RecycleView):
    pass


class ActionBarMain(ActionBar):
    pass


class RootLayout(Label):
    pass


class StatusIcon(Label):
    status = NumericProperty(1)


if __name__ == "__main__":
    DownloaderApp().run()
