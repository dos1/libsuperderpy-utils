#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-win32

pushd .

mkdir build-win32

cd build-win32

cmake ../.. -DCMAKE_TOOLCHAIN_FILE=../../libsuperderpy/cmake/i686-w64-mingw32.toolchain -DCMAKE_BUILD_TYPE=RelWithDebInfo -G Ninja

ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

mkdir rel
cd rel

mkdir "$GAMENAME_PRETTY"

cd "$GAMENAME_PRETTY"

cp ../../src/*.exe ../../src/*.dll ../../src/gamestates/*.dll ../../../libs/win32/* ./
cp -r ../../../../data ./
cp -r ../../../../COPYING ./
rm -rf data/.git
rm -rf data/stuff
rm data/CMakeLists.txt
rm data/$GAMENAME.desktop
rm data/icons/CMakeLists.txt

strip *.exe *.dll

cd ..
rm -rf "../../output/$GAMENAME-win32.zip"
zip -9ry "../../output/$GAMENAME-win32.zip" "$GAMENAME_PRETTY"

popd

rm -rf build-win32
