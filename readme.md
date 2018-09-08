User interface for youtube-dl using the Kivy framework

For the moment, this is just a '''Proof Of Concept''' version, expect malfunctions (see Usage)

# Why

Because there is no (at my knowledge) open source video downloader app for android, and youtube-dl is a well tested downloader
that support a lot of sites.

This app can also be build for systems supported by the Kivy framework

# Usage

* With a web browser, copy the url of the video that you want to download.
* Enter an url in the upper text input
* Clik on the 'Download' button
* Wait unit the video status is 'Done' (under android, unfocus the app will freeze downloads)

# run

 python main.py

# build

With buildozer, I use the docker image jedie/buildozer

# Android

 buildozer android release

## Utils script

Must be run from the root of the project

* signe.sh

Signe the apk

* install.sh

signe the app, uninstall the app on on a connected phone phone then install the app on the phone

The keystore included is needed to signe the app, the password is 123456

Of course an other private key with a strong passphrase must be use in production / submit to a repo


# Issues

android: cannot download on most of the sits due to ssl error

 ERROR: Unable to download JSON metadata: <urlopen error [Errno 1] _ssl.c:503: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure> (caused by URLError(SSLError(1, '_ssl.c:503: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure'),))


tryed with requirements:

 requirements = enum34,pyOpenSSL,openssl,ndg-httpsclient,pyasn1,requests[security],youtube-dl,kivy

got same error
