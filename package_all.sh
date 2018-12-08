#!/bin/bash
set -e

./package_linux_amd64.sh
#./package_linux_i686.sh
./package_win32.sh
./package_win64.sh
./package_osx.sh
./package_html5.sh
./package_wasm.sh
./package_android.sh
./package_maemo.sh
