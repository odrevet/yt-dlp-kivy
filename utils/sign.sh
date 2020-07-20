#!/bin/bash

source utils/config.sh
BUILD_TOOLS_VERSION='30.0.0'
BUILD_TOOLS_DIR=$ANDROID_SDK_DIR/build-tools/$BUILD_TOOLS_VERSION

$BUILD_TOOLS_DIR/zipalign -v -p 4 $BIN/$APP_NAME-0.2-armeabi-v7a-release-unsigned.apk $BIN/$APP_NAME-aligned-unsigned.apk
$BUILD_TOOLS_DIR/apksigner sign --ks mykeystore.keystore --out $BIN/$APP_NAME.apk $BIN/$APP_NAME-aligned-unsigned.apk
