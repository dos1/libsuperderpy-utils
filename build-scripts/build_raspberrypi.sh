#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-raspberrypi

pushd .

mkdir build-raspberrypi

cd build-raspberrypi

cmake -GNinja ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_TOOLCHAIN_FILE=/toolchain/raspberrypi.toolchain
ninja

GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}

GAMENAME_PRETTY=`grep LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL CMakeCache.txt`
GAMENAME_PRETTY=${GAMENAME_PRETTY#LIBSUPERDERPY_GAMENAME_PRETTY:INTERNAL=}

mkdir rel
cd rel

mkdir "$GAMENAME_PRETTY"

cd "$GAMENAME_PRETTY"

cp ../../src/$GAMENAME ../../src/*.so ../../src/gamestates/*.so ./
cp -r ../../../../src ./
cp -r ../../../../libsuperderpy ./
rm -rf libsuperderpy/.git
if [ -d "../../../../cmake" ]; then
  cp -r ../../../../cmake ./
fi
cp -r ../../../../CMakeLists.txt ./
if [ -f "../../../../README" ]; then
  cp -r ../../../../README ./
fi
cp -r ../../../../COPYING ./
cp -r ../../../../data ./
rm -rf data/.git
rm -rf data/stuff

cp $SYSROOT/usr/local/lib/liballegro_acodec.so.5.2 $SYSROOT/usr/local/lib/liballegro_audio.so.5.2 $SYSROOT/usr/local/lib/liballegro_color.so.5.2 $SYSROOT/usr/local/lib/liballegro_font.so.5.2 $SYSROOT/usr/local/lib/liballegro_image.so.5.2 $SYSROOT/usr/local/lib/liballegro_main.so.5.2 $SYSROOT/usr/local/lib/liballegro_memfile.so.5.2 $SYSROOT/usr/local/lib/liballegro_physfs.so.5.2 $SYSROOT/usr/local/lib/liballegro_primitives.so.5.2 $SYSROOT/usr/local/lib/liballegro.so.5.2 $SYSROOT/usr/local/lib/liballegro_ttf.so.5.2 $SYSROOT/usr/local/lib/liballegro_video.so.5.2 $SYSROOT/usr/local/lib/libdumb.so.2 $SYSROOT/usr/local/lib/libFLAC.so.8 $SYSROOT/usr/local/lib/libfreetype.so.6 $SYSROOT/usr/local/lib/libharfbuzz.so $SYSROOT/usr/local/lib/libjpeg.so.8 $SYSROOT/usr/local/lib/libogg.so.0 $SYSROOT/usr/local/lib/libopusfile.so.0 $SYSROOT/usr/local/lib/libopus.so.0 $SYSROOT/usr/local/lib/libpng16.so.16 $SYSROOT/usr/local/lib/libSDL2-2.0.so.0 $SYSROOT/usr/local/lib/libtheoradec.so.1 $SYSROOT/usr/local/lib/libvorbisfile.so.3 $SYSROOT/usr/local/lib/libvorbis.so.0 $SYSROOT/usr/local/lib/libwebp.so.7 $SYSROOT/usr/local/lib/libz.so.1 $SYSROOT/usr/local/lib/libphysfs.so.1 ./

cd ..
rm -rf "../../output/$GAMENAME-raspberrypi.tar.gz"
tar czvf "../../output/$GAMENAME-raspberrypi.tar.gz" "$GAMENAME_PRETTY"

popd

rm -rf build-raspberrypi
