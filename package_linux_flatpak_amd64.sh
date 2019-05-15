#!/bin/sh
mkdir -p ../.assetcache
sudo podman run --rm -i -v `realpath ..`:/src -w /src/utils --privileged dosowisko/libsuperderpy-flatpak-amd64 /src/utils/build-scripts/build_linux_flatpak_amd64.sh $@
