#!/bin/bash

source utils/config.sh

KEYSTORE="${1:-mykeystore.keystore}"
PASS="${2:-123456}"

$BUILD_TOOLS_DIR/zipalign -v -p 4 $BIN/$APP_NAME-$APP_VERSION-$TARGET_ARCH-release-unsigned.apk $BIN/$APP_NAME-aligned-unsigned.apk
$BUILD_TOOLS_DIR/apksigner sign --ks $KEYSTORE --ks-pass pass:"$PASS" --out $BIN/$APP_NAME.apk $BIN/$APP_NAME-aligned-unsigned.apk
