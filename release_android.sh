#!/bin/bash
set -e

SDK_DIR=/home/dos/android/android-sdk-linux/build-tools/24.0.3

if [ -z "$1" ]; then
  echo "Please provide the release number with the arguments."
  exit 1
fi

mkdir -p output

rm -rf build-android

pushd /home/dos/android

. ./env

popd

mkdir build-android

cd build-android

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/android.toolchain -DCMAKE_BUILD_TYPE=Release -DLIBSUPERDERPY_ANDROID_DEBUGGABLE=false -DLIBSUPERDERPY_RELEASE=$1

make -j4

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

cp android/bin/$GAMENAME-debug.apk ../output/$GAMENAME-android-unsigned-unaligned.apk

cd ..
rm -rf build-android


cd output

$SDK_DIR/zipalign -f -v 4 ../output/$GAMENAME-android-unsigned-unaligned.apk ../output/$GAMENAME-android-unsigned.apk

$SDK_DIR/apksigner sign --ks /home/dos/android/android.keystore --out ../output/$GAMENAME-android.apk ../output/$GAMENAME-android-unsigned.apk

rm ../output/$GAMENAME-android-unsigned-unaligned.apk
rm ../output/$GAMENAME-android-unsigned.apk
