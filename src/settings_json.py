import json

settings_json = json.dumps([
    {
        "type": "bool",
        "title": "Verbose",
        "desc": "Print additional info",
        "section": "youtube-dl",
        "key": "verbose"
    },
    {
        "type": "bool",
        "title": "Quiet",
        "desc": "Do not print messages",
        "section": "youtube-dl",
        "key": "quiet"
    },
    {
        "type": "bool",
        "title": "No warning",
        "desc": "Do not print messages",
        "section": "youtube-dl",
        "key": "nowarning"
    },
    {
        "type": "bool",
        "title": "No Check Certificate",
        "desc": "Do not verify SSL certificates",
        "section": "youtube-dl",
        "key": "nocheckcertificate"
    },
    {
        "type": "bool",
        "title": "Prefer insecure",
        "desc": "Use HTTP to retrieve information on YouTube",
        "section": "youtube-dl",
        "key": "prefer_insecure"
    },
    {
        "type": "bool",
        "title": "Ignore errors",
        "desc": "Do not stop on download errors",
        "section": "youtube-dl",
        "key": "ignoreerrors"
    },
    {
        "type": "bool",
        "title": "Call home",
        "desc": "Allow to contact the youtube-dl servers for debugging",
        "section": "youtube-dl",
        "key": "call_home"
    },
    {
        "type": "string",
        "title": "Output template",
        "desc": "Output filename",
        "section": "youtube-dl",
        "key": "outtmpl"
    }
]
)
