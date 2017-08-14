#!/bin/bash
set -e

rm -rf env-android

. $LIBSUPERDERPY_ANDROID_ENV

mkdir env-android

cd env-android

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/android.toolchain -DCMAKE_BUILD_TYPE=RelWithDebInfo

make -j4

bash
