User interface for youtube-dl using the Kivy framework

For the moment, this is just a '''Proof Of Concept''' version, expect malfunctions (see Usage)

# Why

To use youtube-dl with a graphical interface on devices supported by KiVy (for example android)

# Usage

* With a web browser, copy the url of the video that you want to download.
* Enter an url in the upper text input
* Clik on the 'Download' button
* Wait unit the video status is 'Done' (under android, unfocus the app will freeze downloads)

# Dependancies

* youtube-dl

	python -m pip install youtube_dl

* Kivy

	python -m pip install --upgrade --user pip setuptools virtualenv
	python -m pip install kivy

# run (Under Linux)

	python main.py


# Android build (from Ubuntu)

see

* install buildozer

	pip3 install --user --upgrade buildozer

* Install dependencies


```
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade Cython==0.29.19 virtualenv  # the --user should be removed if you do this in a venv

# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/.local/bin/
```

* Build command:

	buildozer android release

At the first run, buildozer will install android depandancies such as ANT, SDK and NDK.

## Utils

Must be run with bash from the project root directory (where this file, readme.md is)

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

The keystore included is needed to signe the app, the password is 123456

* config.sh

Define  variables shared by the utils scripts


# Sources

https://kivy.org/doc/stable/installation/installation-linux.html
https://buildozer.readthedocs.io/en/latest/installation.html
