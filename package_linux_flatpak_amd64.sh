#!/bin/sh
. ./build-scripts/common.sh

$PRIV_DOCKER run --rm -i -v `realpath ..`:/src -w /src/utils $PRIV_ARGS dosowisko/libsuperderpy-flatpak-amd64 /src/utils/build-scripts/build_linux_flatpak_amd64.sh $@
