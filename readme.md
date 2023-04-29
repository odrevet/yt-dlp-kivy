User interface for youtube-dl using the Kivy framework

Documentation assume you are using Python 3 with pip 3.

# Usage

* Past or enter video URL to download in the text field.
* Click on the 'Download' button

# Prerequists

* Kivy (run)
* Buildozer (build for android)

## Docker

I maintain a Dockerfile here https://gist.github.com/odrevet/a9630ed9d9974d88f694a4d4c2a3750c with Kivy and buildozer

```
docker build -t kivy .
docker run -it -v $(pwd):/app kivy bash
pip3 install youtube_dl
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
* https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl
* https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
