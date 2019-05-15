#!/bin/bash
set -e

PATH=$LIBSUPERDERPY_OSXCROSS_ROOT/bin:$PATH

mkdir -p output

rm -rf build-macos

pushd .

mkdir build-macos

cd build-macos

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/osxcross64.toolchain -DCMAKE_BUILD_TYPE=RelWithDebInfo -G Ninja

ninja install

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

cd bin

../../build-scripts/fixup_macos_bundle.rb "$GAMENAME.app"

mv "$GAMENAME.app" "../$GAMENAME_PRETTY.app"

cd ..

rm -rf "../output/$GAMENAME-macos.zip"
zip -9ry "../output/$GAMENAME-macos.zip" "$GAMENAME_PRETTY.app"

popd

rm -rf build-macos
