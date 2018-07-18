#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-linux

pushd .

mkdir build-linux

cd build-linux

schroot --chroot steamrt_scout_amd64 -- cmake ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo  -DUSE_CLANG_TIDY=no -DCMAKE_C_FLAGS="--std=c99"

schroot --chroot steamrt_scout_amd64 -- make -j3

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
cp -r ../../../libs/linux/* ./

cd ..
rm -rf "../../output/$GAMENAME-linux.tar.gz"
tar czvf "../../output/$GAMENAME-linux.tar.gz" "$GAMENAME_PRETTY"

popd

rm -rf build-linux
