#!/bin/bash
set -e

PATH=$LIBSUPERDERPY_OSXCROSS_ROOT/bin:$PATH

mkdir -p output

rm -rf build-osx

pushd .

mkdir build-osx

cd build-osx

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/osxcross64.toolchain -DCMAKE_BUILD_TYPE=RelWithDebInfo -G Ninja

ninja install

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

cd bin

../../fixup_bundle.rb "$GAMENAME.app"

mv "$GAMENAME.app" "../$GAMENAME_PRETTY.app"

cd ..

rm -rf "../output/$GAMENAME-osx.zip"
zip -9ry "../output/$GAMENAME-osx.zip" "$GAMENAME_PRETTY.app"

popd

rm -rf build-osx
