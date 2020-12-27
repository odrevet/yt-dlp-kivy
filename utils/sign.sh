#!/bin/bash

source utils/config.sh
ANDROID_SDK_DIR=~/.buildozer/android/platform/android-sdk
BUILD_TOOLS_VERSION='30.0.3'
BUILD_TOOLS_DIR=$ANDROID_SDK_DIR/build-tools/$BUILD_TOOLS_VERSION
APP_VERSION=0.2.1
TARGET_ARCH=armeabi-v7a

$BUILD_TOOLS_DIR/zipalign -v -p 4 $BIN/$APP_NAME-$APP_VERSION-$TARGET_ARCH-release-unsigned.apk $BIN/$APP_NAME-aligned-unsigned.apk
$BUILD_TOOLS_DIR/apksigner sign --ks mykeystore.keystore --out $BIN/$APP_NAME.apk $BIN/$APP_NAME-aligned-unsigned.apk
