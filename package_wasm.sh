#!/bin/bash
set -e

mkdir -p output

rm -rf build-wasm

. /usr/lib/emsdk/emsdk_env.sh /usr/lib/emsdk

pushd .

mkdir build-wasm

cd build-wasm

emcmake cmake ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DALLEGRO_INCLUDE_PATH=$ALLEGRO_EMSCRIPTEN_DIR/include -DALLEGRO_LIBRARY_PATH=$ALLEGRO_EMSCRIPTEN_DIR/lib/liballegro_monolith-static.a -DCMAKE_INSTALL_PREFIX=output -DUSE_CLANG_TIDY=no -DLIBSUPERDERPY_EMSCRIPTEN_MODE=wasm -G Ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

ninja
ninja ${GAMENAME}_js

cd output/$GAMENAME
mv $GAMENAME.html index.html
zip -9r $GAMENAME-wasm.zip *
mv $GAMENAME-wasm.zip ../../../output/

popd

rm -rf build-wasm
