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

the image can be created with `bash docker/build_buildozer.sh`.

The script `bash docker/run_buildozer.sh` can be used to run a bash in the container. 

Once inside the container, the app can be build normaly using the scripts under the `utils` directory (see `utils` section)

## Dockerfile_vnc

to run yd_dlp_kivy from a docker container and access it from a vnc client

the image can be created with `bash docker/build_vnc.sh` and run with `bash docker/run_vnc.sh`

## Utils

**Must be run using bash**

In case of errors, exported shell variables in `utils/config.sh` may be set

* To build the apk: `build.sh`. 

* To signe the apk: `sign.sh`. The keystore included is needed to signe the app, **the password is 123456**

* To install the apk on a phone: `install.sh`. 

A typical session is :

```bash
bash utils/build.sh
bash utils/sign.sh
bash utils/install.sh
```

# Sources

* https://kivy.org/doc/stable/installation/installation-linux.html
* https://buildozer.readthedocs.io/en/latest/installation.html
* https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
