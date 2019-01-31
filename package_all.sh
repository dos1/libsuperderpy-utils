#!/bin/bash
set -e

docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-linux-amd64 /src/utils/package_linux_amd64.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-linux-i686 /src/utils/package_linux_i686.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-win64 /src/utils/package_win64.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-win32 /src/utils/package_win32.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-macos /src/utils/package_osx.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-android-armv7 /src/utils/package_android.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-emscripten /src/utils/package_wasm.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-emscripten /src/utils/package_html5.sh
docker run --rm -it -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-steamlink /src/utils/package_steamlink.sh
docker run --rm -it -v `realpath ..`:/scratchbox/users/admin/src --privileged --userns=host dosowisko/libsuperderpy-maemo5 "cd /src/utils && ./package_maemo5.sh"
docker run --rm -it -v `realpath ..`:/src -w /src/utils -e ANDROID_KEYSTORE_BASE64="`base64 -w0 $LIBSUPERDERPY_ANDROID_KEYSTORE`" dosowisko/libsuperderpy-android-armv7 /src/utils/release_android.sh git
