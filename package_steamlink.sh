#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-steamlink

pushd .

mkdir build-steamlink

cd build-steamlink

source $MARVELL_SDK_PATH/setenv.sh
cmake ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -GNinja -DCMAKE_TOOLCHAIN_FILE=$MARVELL_SDK_PATH/toolchain/steamlink-toolchain.cmake -DCMAKE_INSTALL_PREFIX=$MARVELL_SDK_PATH/rootfs/usr -DCMAKE_PREFIX_PATH=$MARVELL_SDK_PATH/rootfs
ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

mkdir rel
cd rel

mkdir "$GAMENAME"

cd "$GAMENAME"

cp ../../src/$GAMENAME ../../src/*.so ../../src/gamestates/*.so ./
if [ -f "../../../../README" ]; then
  cp -r ../../../../README ./
fi
cp -r ../../../../COPYING ./
cp -r ../../../../data ./
rm -rf data/.git
rm -rf data/stuff
rm data/CMakeLists.txt
rm data/icons/CMakeLists.txt

cp -r /steamlink-sdk/rootfs/usr/lib/liballegro*.so.5.2 ./

echo "name=$GAMENAME_PRETTY" > toc.txt
echo "icon=data/icons/72/$GAMENAME.png" >> toc.txt
echo "run=$GAMENAME" >> toc.txt

cd ..
rm -rf "../../output/$GAMENAME-steamlink.zip"
zip -9ry "../../output/$GAMENAME-steamlink.zip" "$GAMENAME"

popd

rm -rf build-steamlink
