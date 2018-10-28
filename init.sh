#!/bin/sh
# This script can be used standalone. It creates project named $1 in the current directory.
set -e

git clone https://gitlab.com/dosowisko.net/libsuperderpy-examples.git $1
cd $1
rm -rf .git
git init
git config -f .gitmodules --get-regexp '^submodule\..*\.path$' |
    while read path_key path
    do
        url_key=$(echo $path_key | sed 's/\.path/.url/')
        url=$(git config -f .gitmodules --get "$url_key")
        rmdir $path
        git submodule add https://gitlab.com/dosowisko.net/libsuperderpy-examples.git/$url $path
    done
# TODO: icons, desktop file, gamenames in cmake
git add .
git commit -am "initial commit"
