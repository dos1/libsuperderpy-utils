#!/bin/bash
set -e

GITREV=`cd ..; git rev-list --count HEAD`
if [ -z "$1" ]; then
  read -p "Please provide the version code: [$GITREV] " VERSION_CODE
  if [ -z "$VERSION_CODE" ]; then
    VERSION_CODE="$GITREV"
  fi
else
  if [[ "$1" == "git" ]]; then
    VERSION_CODE=$GITREV
  else
    VERSION_CODE="$1"
  fi
fi

echo "Version code: $VERSION_CODE"

mkdir -p output

rm -rf build-android

pushd .

mkdir build-android

cd build-android

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/android.toolchain -DCMAKE_BUILD_TYPE=Release -DLIBSUPERDERPY_ANDROID_DEBUGGABLE=false -DLIBSUPERDERPY_RELEASE=$VERSION_CODE -DANDROID_TARGET=$LIBSUPERDERPY_ANDROID_TARGET

make -j3

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

cp android/app/build/outputs/apk/debug/app-debug.apk ../output/$GAMENAME-android-armv7-unsigned-unaligned.apk

popd

rm -rf build-android

cd output

# for some reason, this needs to be done twice; maybe there's a way to get gradle to already align the debug apk? (or maybe it's already aligned, just zipalign incompatible?)
$ANDROID_BUILD_TOOLS/zipalign -f -v 4 ../output/$GAMENAME-android-armv7-unsigned-unaligned.apk ../output/$GAMENAME-android-armv7-unsigned-unaligned2.apk || true
$ANDROID_BUILD_TOOLS/zipalign -f -v 4 ../output/$GAMENAME-android-armv7-unsigned-unaligned2.apk ../output/$GAMENAME-android-armv7-unsigned.apk

rm ../output/$GAMENAME-android-armv7-unsigned-unaligned.apk
rm ../output/$GAMENAME-android-armv7-unsigned-unaligned2.apk

TMPKEYFILE=""
KEYSTORE="$ANDROID_KEYSTORE"
if [ -z "$ANDROID_KEYSTORE" ]; then
  if [ "$ANDROID_KEYSTORE_BASE64" ]; then
    KEYSTORE=`mktemp`
    TMPKEYFILE=$KEYSTORE
    echo $ANDROID_KEYSTORE_BASE64 | base64 -d - > $KEYSTORE
  else
    echo "No signing key available, exiting without signing..."
    exit 0
  fi
fi

if [ -z ${ANDROID_KEYSTORE_PASSWORD} ]; then
  $ANDROID_BUILD_TOOLS/apksigner sign --ks $KEYSTORE --out ../output/$GAMENAME-android-armv7.apk ../output/$GAMENAME-android-armv7-unsigned.apk
else
  $ANDROID_BUILD_TOOLS/apksigner sign --ks $KEYSTORE --ks-pass env:ANDROID_KEYSTORE_PASSWORD --out ../output/$GAMENAME-android-armv7.apk ../output/$GAMENAME-android-armv7-unsigned.apk
fi

if [ "$TMPKEYFILE" ]; then
  rm $TMPKEYFILE
fi

rm ../output/$GAMENAME-android-armv7-unsigned.apk
