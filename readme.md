User interface for yt-dlp using the Kivy framework

# Usage

* Past or enter video URL to download in the text field.
* Click on the 'Download' button

# Prerequists

* Kivy (run)
* Buildozer (build for android)

## Docker

There are two Dockerfiles in the `docker` directory

## Dockerfile_buildozer

to build / sign / install the android apk

the image can be created with `bash docker/build_buildozer.sh` and run with `bash/docker/run_buildozer.sh`

## Dockerfile_vnc

to run yd_dlp_kivy from a docker container and access it from a vnc client

the image can be created with `bash docker/build_vnc.sh` and run with `bash/docker/run_vnc.sh`

## Utils

**Must be run using bash**

In case of errors, exported shell variables in `utils/config.sh` may be set

* build.sh

Build the apk

* sign.sh

Signe the apk. The keystore included is needed to signe the app, **the password is 123456**

* install.sh

install the app on the phone

A typical session is :

```
bash utils/build.sh
bash utils/sign.sh
bash utils/install.sh
```


# Sources

* https://kivy.org/doc/stable/installation/installation-linux.html
* https://buildozer.readthedocs.io/en/latest/installation.html
* https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
