import json

general = json.dumps(
    [
        {
            "type": "options",
            "title": "Format method",
            "desc": "Use preset format or detect available formats and ask before download",
            "options": ["Preset", "Ask"],
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
    ]
)
