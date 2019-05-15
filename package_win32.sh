#!/bin/sh
test -t 1 && USE_TTY="-t"
mkdir -p ../.assetcache
podman run --rm -i $USE_TTY -v `realpath ..`:/src -w /src/utils dosowisko/libsuperderpy-win32 /src/utils/build-scripts/build_win32.sh $@
