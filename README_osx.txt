Using osxcross from https://github.com/tpoechtrager/osxcross

Unpack Xcode SDK per instructions in osxcross' README.

Build the osxcross toolchain with:
  CC=clang CXX=clang++ OSX_VERSION_MIN=10.7 ./build.sh

Adjust PATH in current session to contain the shown target directory.

Install Allegro from Macports:
  export MACOSX_DEPLOYMENT_TARGET=10.7
  osxcross-macports install allegro5

Set the environment variable to your osxcross root dir:

LIBSUPERDERPY_OSXCROSS_ROOT=~/git/osxcross/target

and the Xcode SDK version used to prepare the toolchain:

LIBSUPERDERPY_OSXCROSS_SDK_VERSION=10.11

And done! ./package_osx.sh should work now.
