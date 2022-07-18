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

pushd ..

GAMENAME=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_GAMENAME`
GAMENAME_PRETTY=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_GAMENAME_PRETTY`
VENDOR=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_VENDOR`
VERSION=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_VERSION`
GITREV=`cd ..; git rev-list --count HEAD`

if [ -z "$VERSION" ]; then
  VERSION="1.0"
fi

if [ -z "$VENDOR" ]; then
  VENDOR="dosowisko.net"
fi

VERSION="$VERSION-$GITREV"

popd

mkdir rel
cd rel

mkdir "$GAMENAME"

cd "$GAMENAME"

cp ../../src/$GAMENAME ./
if [ -f "../../../../README" ]; then
  cp -r ../../../../README ./
fi
cp -r ../../../../COPYING* ./
cp -r ../../../../data ./
rm -rf data/.git
rm -rf data/stuff
rm -f data/CMakeLists.txt data/icons/CMakeLists.txt

nacptool --create "$GAMENAME_PRETTY" "$VENDOR" "$VERSION" control.nacp
convert data/icons/256/$GAMENAME.png -quality 100 -background white -flatten icon.jpg
elf2nro $GAMENAME $GAMENAME.nro --icon=icon.jpg --nacp=control.nacp
rm $GAMENAME icon.jpg control.nacp

cd ..
rm -rf "../../output/$GAMENAME-switch.zip"
zip -9r "../../output/$GAMENAME-switch.zip" "$GAMENAME"

popd

rm -rf build-switch
