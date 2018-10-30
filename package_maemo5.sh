#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-maemo5

pushd .

mkdir build-maemo5

cd build-maemo5

docker run --rm --privileged -it -v $(realpath ../..):/scratchbox/users/admin/src dosowisko/libsuperderpy-maemo5 "cd /src/utils/build-maemo5 && cmake ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DMAEMO=ON && make -j3"

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

cp -r ../../../libs/maemo5/* ./

cd ..
rm -rf "../../output/$GAMENAME-maemo5.tar.gz"
tar czvf "../../output/$GAMENAME-maemo5.tar.gz" "$GAMENAME_PRETTY"

popd

rm -rf build-maemo5
