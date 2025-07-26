import json
import yt_dlp.utils as utils

# android ffmpeg
import os
from android.storage import app_storage_path
        
cache_dir = os.path.join(app_storage_path(), 'cache')
ffmpeg_path = os.path.join(cache_dir, 'ffmpeg')

ffmpeg_available = utils.check_executable(ffmpeg_path, ['-version']) is not False

format_options = ["Preset"]
if ffmpeg_available:
    format_options.append("Ask")

settings_json = json.dumps(
    [
        {
            "type": "title",
            "title": "General"
        },
        {
            "type": "options",
            "title": "Format method",
            "desc": "Use preset format or detect available formats and ask before download",
            "options": format_options,
            "section": "general",
            "key": "method",
        },
        {
            "type": "options",
            "title": "Preset",
            "desc": "Format preset",
            "options": [
                "best",
                "worst",
                "bestvideo",
                "worstvideo",
                "bestaudio",
                "worstaudio",
            ],
            "section": "general",
            "key": "preset",
        },
        {
            "type": "bool",
            "title": "Ignore errors",
            "desc": "Do not stop on download errors",
            "section": "general",
            "key": "ignoreerrors",
        },
        {
            "type": "path",
            "title": "Download location",
            "desc": "Location where to store downloaded videos",
            "section": "general",
            "key": "savedir",
        },
        {
            "type": "string",
            "title": "Output template",
            "desc": "Template for output names",
            "section": "general",
            "key": "filetmpl",
        },
        {
            "type": "title",
            "title": "Workarounds"
        },
        {
            "type": "bool",
            "title": "No Check Certificate",
            "desc": "Suppress HTTPS certificate validation",
            "section": "workarounds",
            "key": "nocheckcertificate",
        },
        {
            "type": "bool",
            "title": "Prefer insecure",
            "desc": "Use an unencrypted connection to retrieve information about the video (Currently supported only for YouTube)",
            "section": "workarounds",
            "key": "prefer_insecure",
        },
        {
            "type": "title",
            "title": "Verbosity"
        },
        {
            "type": "bool",
            "title": "Quiet",
            "desc": "Activate quiet mode. If used with --verbose, print the log to stderr",
            "section": "verbosity",
            "key": "quiet",
        },
        {
            "type": "bool",
            "title": "No warning",
            "desc": "Ignore warnings",
            "section": "verbosity",
            "key": "nowarning",
        },
    ]
)
