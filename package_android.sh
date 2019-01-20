#!/bin/bash
set -e

mkdir -p output

rm -rf build-android

. $LIBSUPERDERPY_ANDROID_ENV

pushd .

mkdir build-android

cd build-android

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/android.toolchain -DCMAKE_BUILD_TYPE=RelWithDebInfo -DANDROID_TARGET=$LIBSUPERDERPY_ANDROID_TARGET

make -j3

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

cp android/app/build/outputs/apk/debug/app-debug.apk ../output/$GAMENAME-android-debug.apk

popd

rm -rf build-android
