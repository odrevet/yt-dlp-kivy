User interface for yt-dlp using the Kivy framework

# Usage

* Past or enter video URL to download in the text field.
* Click on the 'Download' button

# Prerequists

* Kivy (run)
* Buildozer (build for android)

```
pip install -r requirements.txt
```

## Docker

There are two Dockerfiles in the `docker` directory

## Dockerfile_buildozer

to build / sign / install the android apk

the image can be created with `bash docker/build.sh`.

The script `bash docker/run.sh` can be used to run interactivly a bash in the container. 

Once inside the container, the app can be build normaly using the utils.sh script (see `utils` section)

Or call the utils script directly: 

```
docker run --privileged -v /dev/bus/usb:/dev/bus/usb -v $(pwd):/app buildozer bash -c "bash utils.sh --build --sign"
```

## Dockerfile_vnc

to run yd_dlp_kivy from a docker container and access it from a vnc client

the image can be created with `bash docker/build_vnc.sh` and run with `bash docker/run_vnc.sh`

## Utils

**Must be run using bash**

In case of errors, exported shell variables at the beggining of the script may be adujsted. 

* To build the apk: `--build`. Android SDK will be downloaded at first run. 

* To sign the apk: `--sign`. Keystore (`--key` or `-k`)  and pass (`--pass` or `-p` ) may be passed after this argument. defaults to included test keystore and pass

```
bash utils.sh --sign --key mykeystore.keystore --pass 123456
```

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
