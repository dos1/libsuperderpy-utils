#!/bin/sh
set -e

# TODO: use install target

mkdir -p output

rm -rf build-maemo5

oldpath=`pwd`

mkdir build-maemo5

cd build-maemo5

if [ -e /etc/maemo_version ]; then
  NO_DOCKER=1
fi

if [ -z "$NO_DOCKER" ]; then
  docker run --rm --privileged -v $(realpath ../..):/scratchbox/users/admin/src dosowisko/libsuperderpy-maemo5 "cd /src/utils/build-maemo5 && cmake ../.. -DCMAKE_BUILD_TYPE=Release -DMAEMO5=ON && make -j3"
else
  cmake ../.. -DCMAKE_BUILD_TYPE=Release -DMAEMO5=ON
  make -j3
fi

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

rm -rf build-maemo5
