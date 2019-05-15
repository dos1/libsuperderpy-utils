#!/bin/sh
test -t 1 && USE_TTY="-t"
mkdir -p ../.assetcache
podman run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils -e ANDROID_KEYSTORE_PASSWORD=$LIBSUPERDERPY_ANDROID_KEYSTORE_PASSWORD -e ANDROID_KEYSTORE_BASE64="`base64 -w0 $LIBSUPERDERPY_ANDROID_KEYSTORE`" dosowisko/libsuperderpy-android-armv7 /src/utils/build-scripts/build_android_armv7.sh $@
