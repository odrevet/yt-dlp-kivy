import json

verbosity = json.dumps(
    [
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
