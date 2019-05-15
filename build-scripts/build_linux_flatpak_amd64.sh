#!/bin/bash
set -e

mkdir -p output

rm -rf build-flatpak-amd64 build-flatpak-amd64-repo

pushd .

APPID=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_APPID`
GAMENAME=`build-scripts/read_cmake_var.sh LIBSUPERDERPY_GAMENAME`

cd ..
flatpak-builder utils/build-flatpak-amd64 flatpak/$APPID.json --arch=x86_64 --repo=utils/build-flatpak-amd64-repo
flatpak build-bundle utils/build-flatpak-amd64-repo utils/output/$GAMENAME-linux-amd64.flatpak $APPID --arch=x86_64

popd

rm -rf build-flatpak-amd64 build-flatpak-amd64-repo
