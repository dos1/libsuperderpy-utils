#!/bin/bash
set -e

mkdir -p output

rm -rf build-flatpak-i686 build-flatpak-i686-repo

pushd .

APPID=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_APPID`
GAMENAME=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_GAMENAME`

cd ..
flatpak-builder utils/build-flatpak-i686 flatpak/$APPID.json --arch=i386 --repo=utils/build-flatpak-i686-repo
flatpak build-bundle utils/build-flatpak-i686-repo utils/output/$GAMENAME-linux-i686.flatpak $APPID --arch=i386

popd

rm -rf build-flatpak-i686 build-flatpak-i686-repo
