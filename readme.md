User interface for yt-dlp using the Kivy framework

Documentation assume you are using Python 3 with pip 3.

# Usage

* Past or enter video URL to download in the text field.
* Click on the 'Download' button

# Prerequists

* Kivy (run)
* Buildozer (build for android)

## Docker

Use the Dockerfile, modified from https://gist.github.com/odrevet/a9630ed9d9974d88f694a4d4c2a3750c
contains Kivy and buildozer

```
docker build -t kivy .
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb -v $(pwd):/app kivy bash
```

## Utils

**Must be run using bash**

In case of errors, check utils/config.sh and adjust the exported shell variables

A typical session is :

```
bash utils/build.sh
bash utils/sign.sh
bash utils/install.sh
```

* build.sh

Build the apk

* sign.sh

Signe the apk

* install.sh

uninstall the app on on a connected phone then install the app on the phone

The keystore included is needed to signe the app, **the password is 123456**

* config.sh

Define  variables shared by the utils scripts


# Sources

* https://kivy.org/doc/stable/installation/installation-linux.html
* https://buildozer.readthedocs.io/en/latest/installation.html
* https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp