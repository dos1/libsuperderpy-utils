#!/bin/bash
set -e

mkdir -p output

rm -rf build-html5

. $EMSDK_PATH/emsdk_env.sh $EMSDK_PATH

pushd .

mkdir build-html5

cd build-html5

emcmake cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=$EMSCRIPTEN/system -DCMAKE_INSTALL_PREFIX=output -G Ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

ninja
ninja ${GAMENAME}_js

cd output/$GAMENAME
mv $GAMENAME.html index.html
zip -9r $GAMENAME-html5.zip *
mv $GAMENAME-html5.zip ../../../output/

popd

rm -rf build-html5
