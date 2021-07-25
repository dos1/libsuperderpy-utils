#!/bin/bash
set -e

mkdir -p output

rm -rf build-vita

pushd .

mkdir build-vita

cd build-vita

cmake -GNinja ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_TOOLCHAIN_FILE=/vita.toolchain -DBUILD_SHARED_LIBS=OFF
ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

cp $GAMENAME.vpk ../output/$GAMENAME-vita.vpk

popd

rm -rf build-vita
