#!/bin/sh
test -t 1 && USE_TTY="-t"
mkdir -p ../.assetcache

if [ "$LIBSUPERDERPY_ANDROID_KEYSTORE" ]; then
  LIBSUPERDERPY_ANDROID_KEYSTORE_BASE64="`base64 -w0 $LIBSUPERDERPY_ANDROID_KEYSTORE`"
fi

podman run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils -e ANDROID_KEYSTORE_PASSWORD="$LIBSUPERDERPY_ANDROID_KEYSTORE_PASSWORD" -e ANDROID_KEYSTORE_BASE64="$LIBSUPERDERPY_ANDROID_KEYSTORE_BASE64" dosowisko/libsuperderpy-android-arm64 /src/utils/build-scripts/build_android_arm64.sh $@
