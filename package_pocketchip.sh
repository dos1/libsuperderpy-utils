#!/bin/sh
. ./build-scripts/common.sh

$DOCKER run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-pocketchip /src/utils/build-scripts/build_pocketchip.sh $@
