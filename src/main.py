from kivy.app import App
from kivy.factory import Factory
from kivy.properties import (
    DictProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty,
)
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
    section_options = {
        "general": {
            "bool": [
                "ignore-errors",
                "abort-on-error",
                "ignore-config",
                "flat-playlist",
                "live-from-start",
                "mark-watched",
            ],
            "str": [
                "use-extractors",
                "default-search",
                "plugin-dirs",
                "wait-for-video",
                "color",
                "compat-options",
                "alias",
                "preset-alias",
            ],
        },
        "network": {
            "bool": ["force_ipv4", "force_ipv6", "enable_file_urls"],
            "str": ["proxy", "source_address", "impersonate"],
            "int": ["socket_timeout"],
        },
        "geo": {"str": ["geo_verification_proxy", "xff"]},
        "video_selection": {
            "bool": [
                "no_playlist",
                "yes_playlist",
                "break_match_filters",
                "break_on_existing",
                "break_per_input",
            ],
            "str": [
                "playlist_items",
                "min_filesize",
                "max_filesize",
                "date",
                "datebefore",
                "dateafter",
                "match_filters",
                "download_archive",
            ],
            "int": ["age_limit", "max_downloads", "skip_playlist_after_errors"],
        },
        "download": {
            "bool": [
                "skip_unavailable_fragments",
                "keep_fragments",
                "resize_buffer",
                "playlist_random",
                "lazy_playlist",
                "xattr_set_filesize",
                "hls_use_mpegts",
            ],
            "str": [
                "limit_rate",
                "throttled_rate",
                "download_sections",
                "external_downloader",
                "external_downloader_args",
                "buffer_size",
                "http_chunk_size",
            ],
            "int": [
                "concurrent_fragments",
                "retries",
                "file_access_retries",
                "fragment_retries",
                "retry_sleep",
            ],
        },
        "filesystem": {
            "bool": [
                "restrict_filenames",
                "no_overwrites",
                "force_overwrites",
                "continue",
                "part",
                "mtime",
                "write_description",
                "write_info_json",
                "write_playlist_metafiles",
                "clean_info_json",
                "write_comments",
                "rm_cache_dir",
            ],
            "str": [
                "batch_file",
                "paths",
                "output",
                "output_na_placeholder",
                "load_info_json",
                "cookies",
                "cookies_from_browser",
                "cache_dir",
            ],
            "int": ["windows_filenames", "trim_filenames"],
        },
        "format": {
            "bool": [
                "format_sort_force",
                "video_multistreams",
                "audio_multistreams",
                "prefer_free_formats",
                "check_formats",
            ],
            "str": ["format", "format_sort", "merge_output_format"],
            "int": ["list_formats"],
        },
        "subtitles": {
            "bool": ["write_subs", "write_auto_subs", "list_subs"],
            "str": ["sub_format", "sub_langs"],
        },
        "authentication": {
            "bool": ["netrc", "ap_list_mso"],
            "str": [
                "username",
                "password",
                "twofactor",
                "netrc_location",
                "netrc_cmd",
                "video_password",
                "ap_mso",
                "ap_username",
                "ap_password",
                "client_certificate",
                "client_certificate_key",
                "client_certificate_password",
            ],
        },
        "postprocessing": {
            "bool": [
                "keep_video",
                "post_overwrites",
                "embed_subs",
                "embed_thumbnail",
                "embed_metadata",
                "embed_chapters",
                "embed_info_json",
                "xattrs",
                "split_chapters",
                "force_keyframes_at_cuts",
            ],
            "str": [
                "audio_format",
                "audio_quality",
                "remux_video",
                "recode_video",
                "postprocessor_args",
                "parse_metadata",
                "replace_in_metadata",
                "ffmpeg_location",
                "exec",
                "convert_subs",
                "convert_thumbnails",
                "remove_chapters",
                "use_postprocessor",
                "concat_playlist",
                "fixup",
            ],
            "int": ["extract_audio"],
        },
        "sponsorblock": {
            "bool": ["no_sponsorblock"],
            "str": [
                "sponsorblock_mark",
                "sponsorblock_remove",
                "sponsorblock_chapter_title",
                "sponsorblock_api",
            ],
        },
        "extractor": {
            "bool": ["allow_dynamic_mpd", "hls_split_discontinuity"],
            "str": ["extractor_retries", "extractor_args"],
        },
        "verbosity": {
            "bool": [
                "quiet",
                "no_warnings",
                "ignore_no_formats_error",
                "skip_download",
                "dump_json",
                "dump_single_json",
                "force_write_archive",
                "newline",
                "no_progress",
                "console_title",
                "verbose",
                "dump_pages",
                "write_pages",
                "print_traffic",
            ],
            "str": ["print_template", "print_to_file", "progress_template"],
            "int": ["simulate", "progress_delta"],
        },
        "workarounds": {
            "bool": [
                "legacy_server_connect",
                "no_check_certificates",
                "prefer_insecure",
                "bidi_workaround",
            ],
            "str": [
                "encoding",
                "add_headers",
                "sleep_requests",
                "sleep_interval",
                "max_sleep_interval",
                "sleep_subtitles",
            ],
        },
        "thumbnails": {
            "bool": ["write_thumbnail", "write_all_thumbnails", "list_thumbnails"]
        },
    }

    def get_output_dir(self):
        if platform == "android":
            return os.getenv("EXTERNAL_STORAGE") + "/Download"
        return expanduser("~")

    def init_ydl_opts(self):
        for section, opts in self.section_options.items():
            for key_type, keys in opts.items():
                for key in keys:
                    print(f"get {key}")
                    if not self.config.get(section, key):
                        return

                    if key_type == "bool":
                        self.ydl_opts[key] = self.config.getboolean(section, key)
                    elif key_type == "int":
                        self.ydl_opts[key] = self.config.getint(section, key)
                    elif key_type == "str":
                        self.ydl_opts[key] = self.config.get(section, key)

    def on_config_change(self, config, section, key, value):
        if section not in self.section_options:
            return

        getters = {
            "bool": config.getboolean,
            "int": config.getint,
            "str": lambda s, k: value,
        }

        for typ, keys in self.section_options[section].items():
            if key in keys:
                self.ydl_opts[key] = getters[typ](section, key)
                break

    def build(self):
        if platform == "android" and not check_permission(
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ):
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

        # Config
        config = ConfigParser()
        Config.set("input", "mouse", "mouse,multitouch_on_demand")
        config.read("src/downloader.ini")

        self.config = config
        self.settings_cls = Settings

        self.init_ydl_opts()

        return RootLayout()

    def build_settings(self, settings):
        settings.add_json_panel("General", self.config, "settings/general.json")
        settings.add_json_panel("Network", self.config, "settings/network.json")
        settings.add_json_panel(
            "Geo-restriction", self.config, "settings/geo_restriction.json"
        )
        settings.add_json_panel(
            "Video Selection", self.config, "settings/video_selection.json"
        )
        settings.add_json_panel("Download", self.config, "settings/download.json")
        settings.add_json_panel("Filesystem", self.config, "settings/filesystem.json")
        settings.add_json_panel("Format", self.config, "settings/video_format.json")
        settings.add_json_panel("Subtitles", self.config, "settings/subtitle.json")
        settings.add_json_panel(
            "Authentication", self.config, "settings/authentification.json"
        )
        settings.add_json_panel(
            "Post-Processing", self.config, "settings/post_processing.json"
        )
        settings.add_json_panel(
            "SponsorBlock", self.config, "settings/sponsor_block.json"
        )
        settings.add_json_panel("Extractor", self.config, "settings/extractor.json")
        settings.add_json_panel("Verbosity", self.config, "settings/verbosity.json")
        settings.add_json_panel("Workarounds", self.config, "settings/workarounds.json")


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
