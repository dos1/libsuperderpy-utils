#!/bin/sh
. ./build-scripts/common.sh

$PRIV_DOCKER run --rm -i -v `realpath ..`:/src -w /src/utils $PRIV_ARGS dosowisko/libsuperderpy-flatpak-arm64 /src/utils/build-scripts/build_linux_flatpak_arm64.sh $@

