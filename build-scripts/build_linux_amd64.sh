#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-linux-amd64

pushd .

mkdir build-linux-amd64

cd build-linux-amd64

cmake -GNinja ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo
ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

mkdir rel
cd rel

mkdir "$GAMENAME_PRETTY"

cd "$GAMENAME_PRETTY"

cp ../../src/$GAMENAME ../../src/*.so ../../src/gamestates/*.so ./
cp -r ../../../../src ./
cp -r ../../../../libsuperderpy ./
rm -rf libsuperderpy/.git
if [ -d "../../../../cmake" ]; then
  cp -r ../../../../cmake ./
fi
cp -r ../../../../CMakeLists.txt ./
if [ -f "../../../../README" ]; then
  cp -r ../../../../README ./
fi
cp -r ../../../../COPYING ./
cp -r ../../../../data ./
rm -rf data/.git
rm -rf data/stuff

strip $GAMENAME *.so
cp -r ../../../libs/linux-amd64/* ./

cd ..
rm -rf "../../output/$GAMENAME-linux-amd64.tar.gz"
tar czvf "../../output/$GAMENAME-linux-amd64.tar.gz" "$GAMENAME_PRETTY"

popd

rm -rf build-linux-amd64
