#!/bin/sh
set -e

export PATH=~/git/osxcross/target/bin:$PATH

mkdir -p output

rm -rf build-osx

mkdir build-osx

cd build-osx

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/osxcross64.toolchain -DCMAKE_BUILD_TYPE=RelWithDebInfo

make install -j4

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

PATH=~/git/osxcross/target/bin:$PATH ../fixup_bundle.rb "$GAMENAME.app"

mv "$GAMENAME.app" "$GAMENAME_PRETTY.app"

rm -rf "$GAMENAME_PRETTY.app/Contents/Resources/data"
cp -r ../../data "$GAMENAME_PRETTY.app/Contents/Resources/"

rm -rf "../output/$GAMENAME-osx.zip"
zip -r -y "../output/$GAMENAME-osx.zip" "$GAMENAME_PRETTY.app"

cd ..
rm -rf build-osx
