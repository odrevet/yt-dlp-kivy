import json
import yt_dlp.utils as utils

# Check if ffmpeg is available
ffmpeg_available = utils.check_executable('ffmpeg', ['-version']) is not False

# Format options based on ffmpeg availability
format_options = ["Preset"]
if ffmpeg_available:
    format_options.append("Ask")

settings_json = json.dumps([
    # ===============================
    # GENERAL OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "General Options"
    },
    {
        "type": "bool",
        "title": "Ignore errors",
        "desc": "Ignore download and postprocessing errors",
        "section": "general",
        "key": "ignoreerrors",
    },
    {
        "type": "bool",
        "title": "Update program",
        "desc": "Update this program to the latest version",
        "section": "general",
        "key": "update",
    },
    {
        "type": "string",
        "title": "Default search prefix",
        "desc": "Use this prefix for unqualified URLs (e.g. 'ytsearch:')",
        "section": "general",
        "key": "default_search",
    },
    {
        "type": "bool",
        "title": "Mark videos watched",
        "desc": "Mark videos watched (even with --simulate)",
        "section": "general",
        "key": "mark_watched",
    },
    {
        "type": "options",
        "title": "Color output",
        "desc": "Whether to emit color codes in output",
        "options": ["auto", "always", "never", "no_color"],
        "section": "general",
        "key": "color",
    },

    # ===============================
    # NETWORK OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Network Options"
    },
    {
        "type": "string",
        "title": "Proxy",
        "desc": "Use the specified HTTP/HTTPS/SOCKS proxy",
        "section": "network",
        "key": "proxy",
    },
    {
        "type": "numeric",
        "title": "Socket timeout",
        "desc": "Time to wait before giving up, in seconds",
        "section": "network",
        "key": "socket_timeout",
    },
    {
        "type": "string",
        "title": "Source address",
        "desc": "Client-side IP address to bind to",
        "section": "network",
        "key": "source_address",
    },
    {
        "type": "bool",
        "title": "Force IPv4",
        "desc": "Make all connections via IPv4",
        "section": "network",
        "key": "force_ipv4",
    },
    {
        "type": "bool",
        "title": "Force IPv6",
        "desc": "Make all connections via IPv6",
        "section": "network",
        "key": "force_ipv6",
    },

    # ===============================
    # GEO-RESTRICTION
    # ===============================
    {
        "type": "title",
        "title": "Geo-restriction"
    },
    {
        "type": "string",
        "title": "Geo verification proxy",
        "desc": "Use this proxy to verify the IP address for geo-restricted sites",
        "section": "geo",
        "key": "geo_verification_proxy",
    },
    {
        "type": "string",
        "title": "X-Forwarded-For",
        "desc": "How to fake X-Forwarded-For HTTP header",
        "section": "geo",
        "key": "xff",
    },

    # ===============================
    # VIDEO SELECTION
    # ===============================
    {
        "type": "title",
        "title": "Video Selection"
    },
    {
        "type": "string",
        "title": "Playlist items",
        "desc": "Comma separated playlist_index of items to download (e.g. '1,2,5,8')",
        "section": "selection",
        "key": "playlist_items",
    },
    {
        "type": "string",
        "title": "Minimum filesize",
        "desc": "Abort download if filesize is smaller than SIZE (e.g. 50k or 44.6M)",
        "section": "selection",
        "key": "min_filesize",
    },
    {
        "type": "string",
        "title": "Maximum filesize",
        "desc": "Abort download if filesize is larger than SIZE (e.g. 50k or 44.6M)",
        "section": "selection",
        "key": "max_filesize",
    },
    {
        "type": "string",
        "title": "Date",
        "desc": "Download only videos uploaded on this date (YYYYMMDD)",
        "section": "selection",
        "key": "date",
    },
    {
        "type": "string",
        "title": "Date before",
        "desc": "Download only videos uploaded on or before this date",
        "section": "selection",
        "key": "datebefore",
    },
    {
        "type": "string",
        "title": "Date after",
        "desc": "Download only videos uploaded on or after this date",
        "section": "selection",
        "key": "dateafter",
    },
    {
        "type": "bool",
        "title": "No playlist",
        "desc": "Download only the video, if the URL refers to a video and a playlist",
        "section": "selection",
        "key": "noplaylist",
    },
    {
        "type": "numeric",
        "title": "Age limit",
        "desc": "Download only videos suitable for the given age",
        "section": "selection",
        "key": "age_limit",
    },
    {
        "type": "numeric",
        "title": "Max downloads",
        "desc": "Abort after downloading NUMBER files",
        "section": "selection",
        "key": "max_downloads",
    },

    # ===============================
    # DOWNLOAD OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Download Options"
    },
    {
        "type": "numeric",
        "title": "Concurrent fragments",
        "desc": "Number of fragments that should be downloaded concurrently",
        "section": "download",
        "key": "concurrent_fragment_downloads",
    },
    {
        "type": "string",
        "title": "Rate limit",
        "desc": "Maximum download rate in bytes per second (e.g. 50K or 4.2M)",
        "section": "download",
        "key": "ratelimit",
    },
    {
        "type": "string",
        "title": "Throttled rate",
        "desc": "Minimum download rate below which throttling is assumed",
        "section": "download",
        "key": "throttledratelimit",
    },
    {
        "type": "numeric",
        "title": "Retries",
        "desc": "Number of retries (default is 10)",
        "section": "download",
        "key": "retries",
    },
    {
        "type": "numeric",
        "title": "Fragment retries",
        "desc": "Number of retries for a fragment (default is 10)",
        "section": "download",
        "key": "fragment_retries",
    },
    {
        "type": "bool",
        "title": "Keep fragments",
        "desc": "Keep downloaded fragments on disk after downloading is finished",
        "section": "download",
        "key": "keep_fragments",
    },
    {
        "type": "string",
        "title": "Buffer size",
        "desc": "Size of download buffer (e.g. 1024 or 16K)",
        "section": "download",
        "key": "buffersize",
    },
    {
        "type": "bool",
        "title": "Playlist random",
        "desc": "Download playlist videos in random order",
        "section": "download",
        "key": "playlistrandom",
    },

    # ===============================
    # FILESYSTEM OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Filesystem Options"
    },
    {
        "type": "path",
        "title": "Download location",
        "desc": "Location where to store downloaded videos",
        "section": "filesystem",
        "key": "savedir",
    },
    {
        "type": "string",
        "title": "Output template",
        "desc": "Output filename template",
        "section": "filesystem",
        "key": "filetmpl",
    },
    {
        "type": "bool",
        "title": "Restrict filenames",
        "desc": "Restrict filenames to only ASCII characters, avoid '&' and spaces",
        "section": "filesystem",
        "key": "restrictfilenames",
    },
    {
        "type": "bool",
        "title": "Windows-compatible filenames",
        "desc": "Force filenames to be Windows-compatible",
        "section": "filesystem",
        "key": "windowsfilenames",
    },
    {
        "type": "numeric",
        "title": "Trim filenames length",
        "desc": "Limit the filename length (excluding extension) to the specified number of characters",
        "section": "filesystem",
        "key": "trim_filenames",
    },
    {
        "type": "bool",
        "title": "No overwrites",
        "desc": "Do not overwrite any files",
        "section": "filesystem",
        "key": "nooverwrites",
    },
    {
        "type": "bool",
        "title": "Continue download",
        "desc": "Resume partially downloaded files/fragments",
        "section": "filesystem",
        "key": "continuedl",
    },
    {
        "type": "bool",
        "title": "Use .part files",
        "desc": "Use .part files instead of writing directly into output file",
        "section": "filesystem",
        "key": "part",
    },
    {
        "type": "bool",
        "title": "Use mtime",
        "desc": "Use the Last-modified header to set the file modification time",
        "section": "filesystem",
        "key": "updatetime",
    },
    {
        "type": "bool",
        "title": "Write description",
        "desc": "Write video description to a .description file",
        "section": "filesystem",
        "key": "writedescription",
    },
    {
        "type": "bool",
        "title": "Write info json",
        "desc": "Write video metadata to a .info.json file",
        "section": "filesystem",
        "key": "writeinfojson",
    },
    {
        "type": "bool",
        "title": "Write comments",
        "desc": "Retrieve video comments to be placed in the infojson",
        "section": "filesystem",
        "key": "getcomments",
    },

    # ===============================
    # THUMBNAIL OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Thumbnail Options"
    },
    {
        "type": "bool",
        "title": "Write thumbnail",
        "desc": "Write thumbnail image to disk",
        "section": "thumbnail",
        "key": "writethumbnail",
    },
    {
        "type": "bool",
        "title": "Write all thumbnails",
        "desc": "Write all thumbnail image formats to disk",
        "section": "thumbnail",
        "key": "write_all_thumbnails",
    },

    # ===============================
    # VERBOSITY AND SIMULATION
    # ===============================
    {
        "type": "title",
        "title": "Verbosity and Simulation Options"
    },
    {
        "type": "bool",
        "title": "Quiet",
        "desc": "Activate quiet mode",
        "section": "verbosity",
        "key": "quiet",
    },
    {
        "type": "bool",
        "title": "No warnings",
        "desc": "Ignore warnings",
        "section": "verbosity",
        "key": "no_warnings",
    },
    {
        "type": "bool",
        "title": "Simulate",
        "desc": "Do not download the video and do not write anything to disk",
        "section": "verbosity",
        "key": "simulate",
    },
    {
        "type": "bool",
        "title": "Skip download",
        "desc": "Do not download the video but write all related files",
        "section": "verbosity",
        "key": "skip_download",
    },
    {
        "type": "bool",
        "title": "Dump JSON",
        "desc": "Print JSON information for each video",
        "section": "verbosity",
        "key": "dumpjson",
    },
    {
        "type": "bool",
        "title": "Show progress",
        "desc": "Show progress bar, even if in quiet mode",
        "section": "verbosity",
        "key": "noprogress",
    },
    {
        "type": "bool",
        "title": "Console title",
        "desc": "Display progress in console titlebar",
        "section": "verbosity",
        "key": "consoletitle",
    },
    {
        "type": "bool",
        "title": "Verbose",
        "desc": "Print various debugging information",
        "section": "verbosity",
        "key": "verbose",
    },

    # ===============================
    # WORKAROUNDS
    # ===============================
    {
        "type": "title",
        "title": "Workarounds"
    },
    {
        "type": "string",
        "title": "Encoding",
        "desc": "Force the specified encoding (experimental)",
        "section": "workarounds",
        "key": "encoding",
    },
    {
        "type": "bool",
        "title": "No check certificates",
        "desc": "Suppress HTTPS certificate validation",
        "section": "workarounds",
        "key": "nocheckcertificate",
    },
    {
        "type": "bool",
        "title": "Prefer insecure",
        "desc": "Use an unencrypted connection to retrieve information",
        "section": "workarounds",
        "key": "prefer_insecure",
    },
    {
        "type": "numeric",
        "title": "Sleep requests",
        "desc": "Number of seconds to sleep between requests during data extraction",
        "section": "workarounds",
        "key": "sleep_interval_requests",
    },
    {
        "type": "numeric",
        "title": "Sleep interval",
        "desc": "Number of seconds to sleep before each download",
        "section": "workarounds",
        "key": "sleep_interval",
    },
    {
        "type": "numeric",
        "title": "Max sleep interval",
        "desc": "Maximum number of seconds to sleep",
        "section": "workarounds",
        "key": "max_sleep_interval",
    },

    # ===============================
    # VIDEO FORMAT OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Video Format Options"
    },
    {
        "type": "options",
        "title": "Format method",
        "desc": "Use preset format or detect available formats and ask before download",
        "options": format_options,
        "section": "format",
        "key": "method",
    },
    {
        "type": "options",
        "title": "Preset format",
        "desc": "Format preset when using preset method",
        "options": [
            "best",
            "worst", 
            "bestvideo",
            "worstvideo",
            "bestaudio",
            "worstaudio",
            "best[height<=720]",
            "best[height<=480]",
            "best[height<=360]"
        ],
        "section": "format",
        "key": "preset",
    },
    {
        "type": "string",
        "title": "Format selector",
        "desc": "Video format code (advanced users only)",
        "section": "format",
        "key": "format",
    },
    {
        "type": "string",
        "title": "Format sort",
        "desc": "Sort the formats by the fields given",
        "section": "format",
        "key": "format_sort",
    },
    {
        "type": "bool",
        "title": "List formats",
        "desc": "List available formats of each video",
        "section": "format",
        "key": "listformats",
    },
    {
        "type": "bool",
        "title": "Video multistreams",
        "desc": "Allow multiple video streams to be merged into a single file",
        "section": "format",
        "key": "allow_multiple_video_streams",
    },
    {
        "type": "bool",
        "title": "Audio multistreams", 
        "desc": "Allow multiple audio streams to be merged into a single file",
        "section": "format",
        "key": "allow_multiple_audio_streams",
    },
    {
        "type": "bool",
        "title": "Prefer free formats",
        "desc": "Prefer video formats with free containers over non-free ones",
        "section": "format",
        "key": "prefer_free_formats",
    },
    {
        "type": "string",
        "title": "Merge output format",
        "desc": "Container for merged formats (mp4/mkv/avi/flv/webm/mov)",
        "section": "format",
        "key": "merge_output_format",
    },

    # ===============================
    # SUBTITLE OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Subtitle Options"
    },
    {
        "type": "bool",
        "title": "Write subtitles",
        "desc": "Write subtitle file",
        "section": "subtitle",
        "key": "writesubtitles",
    },
    {
        "type": "bool",
        "title": "Write auto subtitles",
        "desc": "Write automatically generated subtitle file",
        "section": "subtitle",
        "key": "writeautomaticsub",
    },
    {
        "type": "bool",
        "title": "List subtitles",
        "desc": "List available subtitles of each video",
        "section": "subtitle",
        "key": "listsubtitles",
    },
    {
        "type": "string",
        "title": "Subtitle format",
        "desc": "Subtitle format preference (e.g. 'srt' or 'ass/srt/best')",
        "section": "subtitle",
        "key": "subtitlesformat",
    },
    {
        "type": "string",
        "title": "Subtitle languages",
        "desc": "Languages of subtitles to download (e.g. 'en,ja' or 'all')",
        "section": "subtitle",
        "key": "subtitleslangs",
    },

    # ===============================
    # AUTHENTICATION OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Authentication Options"
    },
    {
        "type": "string",
        "title": "Username",
        "desc": "Login with this account ID",
        "section": "authentication",
        "key": "username",
    },
    {
        "type": "string",
        "title": "Password",
        "desc": "Account password",
        "section": "authentication",
        "key": "password",
    },
    {
        "type": "string",
        "title": "Two-factor code",
        "desc": "Two-factor authentication code",
        "section": "authentication",
        "key": "twofactor",
    },
    {
        "type": "bool",
        "title": "Use .netrc",
        "desc": "Use .netrc authentication data",
        "section": "authentication",
        "key": "usenetrc",
    },
    {
        "type": "string",
        "title": "Video password",
        "desc": "Video-specific password",
        "section": "authentication",
        "key": "videopassword",
    },

    # ===============================
    # POST-PROCESSING OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Post-Processing Options"
    },
    {
        "type": "bool",
        "title": "Extract audio",
        "desc": "Convert video files to audio-only files (requires ffmpeg)",
        "section": "postprocessing",
        "key": "extractaudio",
    },
    {
        "type": "options",
        "title": "Audio format",
        "desc": "Format to convert the audio to when extracting",
        "options": ["best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", "wav"],
        "section": "postprocessing",
        "key": "audioformat",
    },
    {
        "type": "string",
        "title": "Audio quality",
        "desc": "Audio quality (0-10 for VBR or specific bitrate like 128K)",
        "section": "postprocessing",
        "key": "audioquality",
    },
    {
        "type": "string",
        "title": "Remux video format",
        "desc": "Remux video into another container if necessary",
        "section": "postprocessing",
        "key": "remuxvideo",
    },
    {
        "type": "string",
        "title": "Recode video format", 
        "desc": "Re-encode the video into another format if necessary",
        "section": "postprocessing",
        "key": "recodevideo",
    },
    {
        "type": "bool",
        "title": "Keep video",
        "desc": "Keep the intermediate video file after post-processing",
        "section": "postprocessing",
        "key": "keepvideo",
    },
    {
        "type": "bool",
        "title": "Embed subtitles",
        "desc": "Embed subtitles in the video (mp4, webm and mkv only)",
        "section": "postprocessing",
        "key": "embedsubs",
    },
    {
        "type": "bool",
        "title": "Embed thumbnail",
        "desc": "Embed thumbnail in the video as cover art",
        "section": "postprocessing",
        "key": "embedthumbnail",
    },
    {
        "type": "bool",
        "title": "Embed metadata",
        "desc": "Embed metadata to the video file",
        "section": "postprocessing",
        "key": "addmetadata",
    },
    {
        "type": "bool",
        "title": "Embed chapters",
        "desc": "Add chapter markers to the video file",
        "section": "postprocessing",
        "key": "addchapters",
    },
    {
        "type": "bool",
        "title": "Write xattrs",
        "desc": "Write metadata to the video file's xattrs",
        "section": "postprocessing",
        "key": "xattrs",
    },
    {
        "type": "options",
        "title": "Fixup policy",
        "desc": "Automatically correct known faults of the file",
        "options": ["never", "warn", "detect_or_warn", "force"],
        "section": "postprocessing",
        "key": "fixup",
    },
    {
        "type": "string",
        "title": "FFmpeg location",
        "desc": "Location of the ffmpeg binary",
        "section": "postprocessing",
        "key": "ffmpeg_location",
    },
    {
        "type": "string",
        "title": "Convert subtitles",
        "desc": "Convert subtitles to another format (ass, lrc, srt, vtt)",
        "section": "postprocessing",
        "key": "convertsubtitles",
    },
    {
        "type": "string",
        "title": "Convert thumbnails",
        "desc": "Convert thumbnails to another format (jpg, png, webp)",
        "section": "postprocessing",
        "key": "convertthumbnails",
    },
    {
        "type": "bool",
        "title": "Split chapters",
        "desc": "Split video into multiple files based on internal chapters",
        "section": "postprocessing",
        "key": "splitchapters",
    },

    # ===============================
    # SPONSORBLOCK OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "SponsorBlock Options"
    },
    {
        "type": "string",
        "title": "SponsorBlock mark",
        "desc": "SponsorBlock categories to create chapters for (sponsor,intro,outro,etc.)",
        "section": "sponsorblock",
        "key": "sponsorblock_mark",
    },
    {
        "type": "string",
        "title": "SponsorBlock remove",
        "desc": "SponsorBlock categories to be removed from the video file",
        "section": "sponsorblock",
        "key": "sponsorblock_remove",
    },
    {
        "type": "string",
        "title": "SponsorBlock API URL",
        "desc": "SponsorBlock API location (default: https://sponsor.ajay.app)",
        "section": "sponsorblock",
        "key": "sponsorblock_api",
    },

    # ===============================
    # EXTRACTOR OPTIONS
    # ===============================
    {
        "type": "title",
        "title": "Extractor Options"
    },
    {
        "type": "numeric",
        "title": "Extractor retries",
        "desc": "Number of retries for known extractor errors (default is 3)",
        "section": "extractor",
        "key": "extractor_retries",
    },
    {
        "type": "bool",
        "title": "Allow dynamic MPD",
        "desc": "Process dynamic DASH manifests",
        "section": "extractor",
        "key": "dynamic_mpd",
    },
    {
        "type": "bool",
        "title": "HLS split discontinuity",
        "desc": "Split HLS playlists to different formats at discontinuities",
        "section": "extractor",
        "key": "hls_split_discontinuity",
    },
])
