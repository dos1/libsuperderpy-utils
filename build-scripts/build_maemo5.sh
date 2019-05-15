#!/bin/sh
set -e

# TODO: use install target

mkdir -p output

rm -rf build-maemo5

oldpath=`pwd`

mkdir build-maemo5

cd build-maemo5

cmake ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DMAEMO5=ON
make -j3

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

mkdir rel
cd rel

mkdir "$GAMENAME_PRETTY"

cd "$GAMENAME_PRETTY"

cp ../../src/$GAMENAME ../../src/*.so ../../src/gamestates/*.so ./
cp -r ../../../../COPYING ./
cp -r ../../../../data ./
rm -rf data/.git
rm -rf data/stuff

cp -r ../../../libs/maemo5/* ./

cd ..
rm -rf "../../output/$GAMENAME-maemo5.tar.gz"
tar czvf "../../output/$GAMENAME-maemo5.tar.gz" "$GAMENAME_PRETTY"

cd $oldpath

rm -rf build-maemo5 || true
