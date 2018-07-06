#!/bin/bash
set -e

mkdir -p output

rm -rf build-html5

. /usr/lib/emsdk/emsdk_env.sh /usr/lib/emsdk

pushd .

mkdir build-html5

cd build-html5

emcmake cmake ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DALLEGRO_INCLUDE_PATH=$ALLEGRO_EMSCRIPTEN_DIR/include -DALLEGRO_LIBRARY_PATH=$ALLEGRO_EMSCRIPTEN_DIR/lib/liballegro_monolith-static.a -DCMAKE_INSTALL_PREFIX=output -DUSE_CLANG_TIDY=no -G Ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

ninja
ninja ${GAMENAME}_js

cd output/$GAMENAME
zip -9r $GAMENAME-html5.zip *
mv $GAMENAME-html5.zip ../../../output/

popd

rm -rf build-html5
