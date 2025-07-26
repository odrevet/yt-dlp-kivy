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

see `Dockerfile`

* Build with:

`docker build -t buildozer .`

* Call the utils script to build or sign:

`docker run -it --user root -v $(pwd):/root -v ~/.buildozer:/root/.buildozer buildozer /bin/bash -c "bash utils.sh --build"`

* or build directly using buildozer

`docker run -it --user root -v $(pwd):/root -v ~/.buildozer:/root/.buildozer buildozer bash -c "yes | buildozer android release"`

* To open a bash shell

`docker run -it --user root -v $(pwd):/root -v ~/.buildozer:/root/.buildozer buildozer`

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

```sh
rm -rf .buildozer
```

* logcat

```sh
adb logcat --pid=$(adb shell pidof fr.odrevet.youtube_dl_kivy) | grep -E "(ERROR|python|File|line)"
```

* access filesytem

```sh
buildozer android debug
adb install bin/youtube_dl_kivy-0.5.0-arm64-v8a-debug.apk
adb shell
run-as fr.odrevet.youtube_dl_kivy
cd /data/data/fr.odrevet.youtube_dl_kivy/files
```

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
