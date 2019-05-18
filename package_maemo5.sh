#!/bin/sh
. ./build-scripts/common.sh

$PRIV_DOCKER run --rm -i $USE_TTY -v `realpath ..`:/scratchbox/users/admin/src $PRIV_ARGS dosowisko/libsuperderpy-maemo5 "cd /src/utils && ./build-scripts/build_maemo5.sh $@"
