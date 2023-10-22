#!/usr/bin/env bash

# Read the buildozer.spec file and extract version and package.domain
APP_VERSION=$(grep "version =" buildozer.spec | awk -F "=" '{print $2}' | tr -d '[:space:]')
APP_NAME=$(grep "package.name =" buildozer.spec | awk -F "=" '{print $2}' | tr -d '[:space:]')

BIN='bin'
ANDROID_SDK_DIR=~/.buildozer/android/platform/android-sdk
PACKAGE=fr.odrevet.$APP_NAME
BUILD_TOOLS_VERSION='34.0.0'
BUILD_TOOLS_DIR=$ANDROID_SDK_DIR/build-tools/$BUILD_TOOLS_VERSION
TARGET_ARCH=arm64-v8a

usage() {
  echo "arguments: "
  echo "--build"
  echo "--sign"
  echo "--install"
}

while true; do
  action=$1
  echo $action
  case "$1" in
  --build)
    shift
    
    buildozer android release
    ;;
  --sign)
    shift

    if [[ $1 != --* ]]; then
      KEYSTORE=$1
      shift
    else
      KEYSTORE=mykeystore.keystore
    fi

    if [[ $1 != --* ]]; then
      PASS=$1
      shift
    else
      PASS=123456
    fi

    RELEASE_UNSIGNED=$BIN/$APP_NAME-$APP_VERSION-$TARGET_ARCH-release-unsigned.apk
    RELEASE_ALIGNED=$BIN/$APP_NAME-aligned-unsigned.apk
    OUT=$BIN/$APP_NAME.apk

    $BUILD_TOOLS_DIR/zipalign -v -f -p 4 $RELEASE_UNSIGNED $RELEASE_ALIGNED
    $BUILD_TOOLS_DIR/apksigner sign --ks $KEYSTORE --ks-pass pass:"$PASS" --out $OUT $RELEASE_ALIGNED

    ;;
  --install)
    shift

    $PLATEFORM_TOOLS_DIR=$ANDROID_SDK_DIR/platform-tools
    $PLATEFORM_TOOLS_DIR/adb uninstall $PACKAGE
    $PLATEFORM_TOOLS_DIR/adb install $BIN/$APP_NAME.apk
   
    ;;
  --logcat)
    shift
   
    $PLATEFORM_TOOLS_DIR=$ANDROID_SDK_DIR/platform-tools
    $PLATEFORM_TOOLS_DIR/adb logcat | grep $PACKAGE  
   
    ;;
  *) break ;;
  esac
done
