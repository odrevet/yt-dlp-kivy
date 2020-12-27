User interface for youtube-dl using the Kivy framework

Documentation assume you are using Python 3 with pip 3.

# Usage

* With a web browser, copy the url of the video that you want to download.
* Enter an url in the upper text input
* Clik on the 'Download' button

# Dependancies

	pip install kivy[full] youtube_dl

# run (Desktop)

    python main.py


# Android build (from Ubuntu)

See https://buildozer.readthedocs.io/en/latest/installation.html


```
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip install --user --upgrade Cython==0.29.19 virtualenv buildozer

# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/.local/bin/
```

* Build command:

    buildozer android release

At the first run, buildozer will install android depandancies such as ANT, SDK and NDK.

* Build and install debug version

    buildozer android debug deploy run

## Utils

**Must be run using bash** from the project root directory (where this file, readme.md is)

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
