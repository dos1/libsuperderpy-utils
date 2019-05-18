#!/bin/sh
. ./build-scripts/common.sh

$DOCKER run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-linux-amd64 /src/utils/build-scripts/build_linux_amd64.sh $@
