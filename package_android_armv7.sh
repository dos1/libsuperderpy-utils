#!/bin/sh
. ./build-scripts/common.sh

if [ "$LIBSUPERDERPY_ANDROID_KEYSTORE" ]; then
  LIBSUPERDERPY_ANDROID_KEYSTORE_BASE64="`base64 -w0 $LIBSUPERDERPY_ANDROID_KEYSTORE`"
fi

$DOCKER run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils -e ANDROID_KEYSTORE_PASSWORD="$LIBSUPERDERPY_ANDROID_KEYSTORE_PASSWORD" -e ANDROID_KEYSTORE_BASE64="$LIBSUPERDERPY_ANDROID_KEYSTORE_BASE64" dosowisko/libsuperderpy-android-armv7 /src/utils/build-scripts/build_android_armv7.sh $@
