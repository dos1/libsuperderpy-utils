#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Please provide the release number with the arguments."
  exit 1
fi

mkdir -p output

rm -rf build-android

. $LIBSUPERDERPY_ANDROID_ENV

pushd .

mkdir build-android

cd build-android

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/android.toolchain -DCMAKE_BUILD_TYPE=Release -DLIBSUPERDERPY_ANDROID_DEBUGGABLE=false -DLIBSUPERDERPY_RELEASE=$1 -DANDROID_TARGET=$LIBSUPERDERPY_ANDROID_TARGET -DUSE_CLANG_TIDY=no

make -j3

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

cp android/bin/$GAMENAME-debug.apk ../output/$GAMENAME-android-unsigned-unaligned.apk

popd

rm -rf build-android

cd output

$ANDROID_BUILD_TOOLS/zipalign -f -v 4 ../output/$GAMENAME-android-unsigned-unaligned.apk ../output/$GAMENAME-android-unsigned.apk

$ANDROID_BUILD_TOOLS/apksigner sign --ks $ANDROID_KEYSTORE --out ../output/$GAMENAME-android.apk ../output/$GAMENAME-android-unsigned.apk

rm ../output/$GAMENAME-android-unsigned-unaligned.apk
rm ../output/$GAMENAME-android-unsigned.apk

cd ..
