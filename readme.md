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
docker run -rm -v $(pwd):/app buildozer bash -c "bash utils.sh --build --sign"
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

* When build, if requested API cannot be found then the buildozer directory must be cleared

`rm -rf .buildozer`

* Debug

`adb logcat --pid=$(adb shell pidof fr.odrevet.youtube_dl_kivy.youtube_dl_kivy) | grep -E "(ERROR|python|File|line)"`


# CI testing with act

## Create env file with dummy keystore

```
cat > .env.act << EOF
GITHUB_TOKEN=dummy_token_for_testing
KEYSTORE_BASE64=$(base64 -w 0 mykeystore.keystore)
KEYSTORE_PASSPHRASE=123456
EOF
```

## Run

* check syntax

```
act workflow_dispatch --dry-run
```

* with verbose output

```
act workflow_dispatch --env-file .env.act --verbose
```

# Sources

* https://kivy.org/doc/stable/installation/installation-linux.html
* https://buildozer.readthedocs.io/en/latest/installation.html
* https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
