import json

settings_json = json.dumps([
    {
        "type": "options",
        "title": "Format method",
        "desc": "Set which method to use to select the format",
        "options": ["Preset", "Custom", "Ask"],
        "section": "general",
        "key": "method"
    },
    {
        "type": "string",
        "title": "Custom format",
        "desc": "Format",
        "section": "general",
        "key": "custom"
    },
    {
        "type": "options",
        "title": "Preset",
        "desc": "Format preset",
        "options": ["best", "worst", "bestvideo", "worstvideo", "bestaudio", "worstaudio"],
        "section": "general",
        "key": "preset"
    },
    {
        "type": "bool",
        "title": "Quiet",
        "desc": "Do not print messages",
        "section": "general",
        "key": "quiet"
    },
    {
        "type": "bool",
        "title": "No warning",
        "desc": "Do not print messages",
        "section": "general",
        "key": "nowarning"
    },
    {
        "type": "bool",
        "title": "No Check Certificate",
        "desc": "Do not verify SSL certificates",
        "section": "general",
        "key": "nocheckcertificate"
    },
    {
        "type": "bool",
        "title": "Prefer insecure",
        "desc": "Use HTTP to retrieve information on YouTube",
        "section": "general",
        "key": "prefer_insecure"
    },
    {
        "type": "bool",
        "title": "Ignore errors",
        "desc": "Do not stop on download errors",
        "section": "general",
        "key": "ignoreerrors"
    },
    {
        "type": "bool",
        "title": "Call home",
        "desc": "Allow to contact the general servers for debugging",
        "section": "general",
        "key": "call_home"
    },
    {
        "type": "path",
        "title": "Download location",
        "desc": "Location where to store downloaded videos",
        "section": "general",
        "key": "savedir"
    }

]
)
