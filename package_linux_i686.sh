#!/bin/sh
. ./build-scripts/common.sh

$DOCKER run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-linux-i686 /src/utils/build-scripts/build_linux_i686.sh $@
