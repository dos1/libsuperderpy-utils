#!/bin/bash
set -e

# TODO: use install target

mkdir -p output

rm -rf build-pocketchip

pushd .

mkdir build-pocketchip

cd build-pocketchip

cmake -GNinja ../.. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DPOCKETCHIP=1
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

cp /usr/local/lib/liballegro_acodec.so.5.2 /usr/local/lib/liballegro_audio.so.5.2 /usr/local/lib/liballegro_color.so.5.2 /usr/local/lib/liballegro_font.so.5.2 /usr/local/lib/liballegro_image.so.5.2 /usr/local/lib/liballegro_main.so.5.2 /usr/local/lib/liballegro_memfile.so.5.2 /usr/local/lib/liballegro_physfs.so.5.2 /usr/local/lib/liballegro_primitives.so.5.2 /usr/local/lib/liballegro.so.5.2 /usr/local/lib/liballegro_ttf.so.5.2 /usr/local/lib/liballegro_video.so.5.2 /usr/local/lib/libdumb.so.2 /usr/local/lib/libFLAC.so.8 /usr/local/lib/libfreetype.so.6 /usr/local/lib/libharfbuzz.so /usr/local/lib/libjpeg.so.8 /usr/local/lib/libogg.so.0 /usr/local/lib/libopusfile.so.0 /usr/local/lib/libopus.so.0 /usr/local/lib/libpng16.so.16 /usr/local/lib/libSDL2-2.0.so.0 /usr/local/lib/libtheoradec.so.1 /usr/local/lib/libvorbisfile.so.3 /usr/local/lib/libvorbis.so.0 /usr/local/lib/libwebp.so.7 /usr/local/lib/libz.so.1 /usr/local/lib/libphysfs.so.1 ./

cd ..
rm -rf "../../output/$GAMENAME-pocketchip.tar.gz"
tar czvf "../../output/$GAMENAME-pocketchip.tar.gz" "$GAMENAME_PRETTY"

popd

rm -rf build-pocketchip
