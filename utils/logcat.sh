#!/bin/bash

source utils/config.sh

PLATEFORM_TOOLS_DIR=$ANDROID_SDK_DIR/platform-tools
$PLATEFORM_TOOLS_DIR/adb logcat | grep $PACKAGE
