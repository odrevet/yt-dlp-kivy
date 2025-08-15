#!/usr/bin/env bash

# Read the buildozer.spec file and extract version and package.domain
# Allow environment variables to override default values
APP_VERSION=${APP_VERSION:-$(sed -n 's/.*["'\'']\([0-9.]*\)["'\''].*/\1/p' src/_version.py)}
APP_NAME=${APP_NAME:-$(grep "package.name =" buildozer.spec | awk -F "=" '{print $2}' | tr -d '[:space:]')}
BIN=${BIN:-'bin'}
ANDROID_SDK_DIR=${ANDROID_SDK_DIR:-~/.buildozer/android/platform/android-sdk}
PACKAGE=${PACKAGE:-fr.odrevet.$APP_NAME}
TARGET_ARCH=${TARGET_ARCH:-$(grep "android.arch =" buildozer.spec | awk -F "=" '{print $2}' | tr -d '[:space:]')}

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
    
    yes | buildozer android release
    ;;
  --sign)
    shift

   while [[ $# -gt 0 ]]; do
      case "$1" in
        --key|-k)
          KEYSTORE=$2
          shift 2
          ;;
        --pass|-p)
          PASS=$2
          shift 2
          ;;
        *)
          break
          ;;
      esac
    done

    if [[ -z "$KEYSTORE" ]]; then
      KEYSTORE="mykeystore.keystore"
      echo "No keystore specified, using default: $KEYSTORE"
    fi

    if [[ -z "$PASS" ]]; then
      PASS="123456"
      echo "No keystore password specified, using default: $PASS"
    fi
    
    RELEASE_UNSIGNED=$BIN/$APP_NAME-$APP_VERSION-$TARGET_ARCH-release-unsigned.apk
    RELEASE_ALIGNED=$BIN/$APP_NAME-aligned-unsigned.apk
    OUT=$BIN/$APP_NAME.apk

    BUILD_TOOLS_VERSION=$(grep -oP "buildToolsVersion '\K[^']+" ./.buildozer/android/platform/build-$TARGET_ARCH/dists/$APP_NAME/build.gradle)
    BUILD_TOOLS_DIR=$ANDROID_SDK_DIR/build-tools/$BUILD_TOOLS_VERSION

    $BUILD_TOOLS_DIR/zipalign -v -f -p 4 $RELEASE_UNSIGNED $RELEASE_ALIGNED

    $BUILD_TOOLS_DIR/apksigner sign --ks $KEYSTORE --ks-pass pass:"$PASS" --in $RELEASE_ALIGNED --out $OUT

    ;;
  --install)
    shift

    PLATEFORM_TOOLS_DIR=$ANDROID_SDK_DIR/platform-tools
    $PLATEFORM_TOOLS_DIR/adb uninstall $PACKAGE
    $PLATEFORM_TOOLS_DIR/adb install $BIN/$APP_NAME.apk
   
    ;;
  --logcat)
    shift
   
    PLATEFORM_TOOLS_DIR=$ANDROID_SDK_DIR/platform-tools
    $PLATEFORM_TOOLS_DIR/adb logcat | grep $PACKAGE  
   
    ;;
  *) break ;;
  esac
done
