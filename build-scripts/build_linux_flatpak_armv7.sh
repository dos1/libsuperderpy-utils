#!/bin/bash
set -e

mkdir -p output

rm -rf build-flatpak-armv7 build-flatpak-armv7-repo

pushd .

APPID=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_APPID`
GAMENAME=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_GAMENAME`

cd ..
update-binfmts --enable qemu-arm
flatpak-builder utils/build-flatpak-armv7 flatpak/$APPID.json --arch=arm --repo=utils/build-flatpak-armv7-repo
flatpak build-bundle utils/build-flatpak-armv7-repo utils/output/$GAMENAME-linux-armv7.flatpak $APPID --arch=arm

popd

rm -rf build-flatpak-armv7 build-flatpak-armv7-repo
