#!/bin/sh
set -e

./package_linux.sh
./package_win32.sh
./package_win64.sh
./package_osx.sh
./package_android.sh
