#!/bin/sh
test -t 1 && USE_TTY="-t"
mkdir -p ../.assetcache
podman run --rm -i $USE_TTY -v `realpath ..`:/scratchbox/users/admin/src --privileged dosowisko/libsuperderpy-maemo5 "cd /src/utils && ./build-scripts/build_maemo5.sh $@" # with docker, add "--userns=host"
