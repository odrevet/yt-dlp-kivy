import json

workarounds = json.dumps(
    [

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
    ]
)
