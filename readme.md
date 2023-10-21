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

In case of errors, exported shell variables at the beggining of the script may be adujsted. 

* To build the apk: `--build`. Android SDK will be downloaded at first run. 

* To sign the apk: `--sign`. Keystore and pass may be passed after this argument, or will defaults to included test keystore

* To install the apk: `--install`. 

Example: 

```bash
bash utils.sh --build --sign --install
```


# troubleshooting

* Requested API cannot be found

`rm -rf .buildozer`

# Sources

* https://kivy.org/doc/stable/installation/installation-linux.html
* https://buildozer.readthedocs.io/en/latest/installation.html
* https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
