#!/bin/bash
set -e

mkdir -p output

rm -rf build-flatpak-arm64 build-flatpak-arm64-repo

pushd .

APPID=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_APPID`
GAMENAME=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_GAMENAME`

cd ..
update-binfmts --enable qemu-aarch64
flatpak-builder utils/build-flatpak-arm64 flatpak/$APPID.json --arch=aarch64 --repo=utils/build-flatpak-arm64-repo
flatpak build-bundle utils/build-flatpak-arm64-repo utils/output/$GAMENAME-linux-arm64.flatpak $APPID --arch=aarch64

popd

rm -rf build-flatpak-arm64 build-flatpak-arm64-repo
