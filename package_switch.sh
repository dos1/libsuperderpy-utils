#!/bin/sh
. ./build-scripts/common.sh

$DOCKER run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-switch /src/utils/build-scripts/build_switch.sh $@
