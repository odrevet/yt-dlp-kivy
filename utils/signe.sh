BIN='bin'
APP_NAME='VideoDownloader'
BUILD_TOOLS_VERSION='28.0.2'
rm bin/my-app-unsigned-aligned.apk bin/my-app-unsigned-aligned.apk
/opt/android-sdk/build-tools/$BUILD_TOOLS_VERSION/zipalign -v -p 4 $BIN/$APP_NAME-0.1-release-unsigned.apk $BIN/my-app-unsigned-aligned.apk
/opt/android-sdk/build-tools/$BUILD_TOOLS_VERSION/apksigner sign --ks mykeystore.keystore --out $BIN/my-app-release.apk $BIN/my-app-unsigned-aligned.apk
