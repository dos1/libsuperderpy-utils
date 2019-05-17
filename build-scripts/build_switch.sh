#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-switch

pushd .

mkdir build-switch

cd build-switch

source /opt/devkitpro/switchvars.sh

cmake -GNinja ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_TOOLCHAIN_FILE=/switch.toolchain
ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

mkdir rel
cd rel

mkdir "$GAMENAME"

cd "$GAMENAME"

cp ../../src/$GAMENAME ./
if [ -f "../../../../README" ]; then
  cp -r ../../../../README ./
fi
cp -r ../../../../COPYING ./
cp -r ../../../../data ./
rm -rf data/.git
rm -rf data/stuff
rm -f data/CMakeLists.txt data/icons/CMakeLists.txt

elf2nro $GAMENAME $GAMENAME.nro --icon=data/icons/$GAMENAME.png
rm $GAMENAME

cd ..
rm -rf "../../output/$GAMENAME-switch.tar.gz"
zip -9r "../../output/$GAMENAME-switch.zip" "$GAMENAME"

popd

rm -rf build-switch
