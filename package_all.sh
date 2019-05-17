#!/bin/bash
set -e

./package_maemo5.sh
./package_linux_flatpak_arm64.sh
#./package_linux_flatpak_armv7.sh # requires SDL backend in flatpak manifest
./package_linux_flatpak_amd64.sh
#./package_linux_flatpak_i686.sh # requires SDL backend in flatpak manifest
./package_linux_amd64.sh
./package_linux_i686.sh
./package_win64.sh
./package_win32.sh
./package_macos.sh
./package_wasm.sh
./package_html5.sh
./package_steamlink.sh
./package_raspberrypi.sh
./package_pocketchip.sh
./package_switch.sh
./package_android_armv7.sh git
