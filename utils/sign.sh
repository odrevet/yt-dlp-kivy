#!/bin/bash

source utils/config.sh

$BUILD_TOOLS_DIR/zipalign -v -p 4 $BIN/$APP_NAME-$APP_VERSION-$TARGET_ARCH-release-unsigned.apk $BIN/$APP_NAME-aligned-unsigned.apk
$BUILD_TOOLS_DIR/apksigner sign --ks mykeystore.keystore --out $BIN/$APP_NAME.apk $BIN/$APP_NAME-aligned-unsigned.apk
