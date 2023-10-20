#!/bin/bash

# Read the buildozer.spec file and extract version and package.domain
APP_VERSION=$(grep "version =" buildozer.spec | awk -F "=" '{print $2}' | tr -d '[:space:]')
APP_NAME=$(grep "package.name =" buildozer.spec | awk -F "=" '{print $2}' | tr -d '[:space:]')

BIN='bin'
ANDROID_SDK_DIR=~/.buildozer/android/platform/android-sdk
PACKAGE=fr.odrevet.$APP_NAME
BUILD_TOOLS_VERSION='34.0.0'
BUILD_TOOLS_DIR=$ANDROID_SDK_DIR/build-tools/$BUILD_TOOLS_VERSION
TARGET_ARCH=arm64-v8a_armeabi-v7a
