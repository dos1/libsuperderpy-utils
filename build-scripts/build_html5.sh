#!/bin/bash
set -e

mkdir -p output

rm -rf build-html5

pushd .

mkdir build-html5

cd build-html5

SRC_DIR=`realpath ../../`

emcmake cmake "$SRC_DIR" -DCMAKE_BUILD_TYPE=Release -DCMAKE_SYSROOT=$EMSCRIPTEN/system/local -DCMAKE_PREFIX_PATH=$EMSCRIPTEN/system/local -DAllegro5_LIBRARY=$EMSCRIPTEN/system/local/lib/allegro5.so -DCMAKE_INSTALL_PREFIX=output -DLIBSUPERDERPY_EMSCRIPTEN_MODE=asm.js -G Ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

ninja
ninja ${GAMENAME}_js

cd output/$GAMENAME
mv $GAMENAME.html index.html
rm -rf gamestates
if [ -d "$SRC_DIR/html" ]; then
  cp -r "$SRC_DIR"/html/* ./
fi

zip -0r $GAMENAME-html5.zip *
mv $GAMENAME-html5.zip ../../../output/

popd

rm -rf build-html5
