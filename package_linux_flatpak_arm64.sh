#!/bin/sh
mkdir -p ../.assetcache
sudo podman run --rm -i -v `realpath ..`:/src -w /src/utils --privileged dosowisko/libsuperderpy-flatpak-arm64 /src/utils/build-scripts/build_linux_flatpak_arm64.sh $@

