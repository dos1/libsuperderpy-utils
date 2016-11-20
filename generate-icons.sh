#!/bin/bash
set -e

if [ "$#" -lt 1 ]; then
  echo "Usage: ./generate {png,svg} [--pixelart]"
  exit 1
fi

rm -rf build-icons
mkdir build-icons
cd build-icons
cmake ../..
GAMENAME=`grep LIBSUPERDERPY_GAMENAME:INTERNAL CMakeCache.txt`
GAMENAME=${GAMENAME#LIBSUPERDERPY_GAMENAME:INTERNAL=}
cd ..
rm -rf build-icons

cd ../data/icons

FILE=$GAMENAME.$1
SIZES="16 32 48 64 128 256 512 1024"
ICOSIZES="16 32 48 64"
PNGSIZES="128 256 512 1024" 
MACSIZES="128 256 512 1024"
ICOFILELIST=
PNGFILELIST=
MACFILELIST=

INTERPOLATION=spline

if [[ "$2" == "--pixelart" ]]
then
  INTERPOLATION=nearest-neighbor
fi

if [[ ! -e "$FILE" ]]
then
  echo File $FILE does not exist!
  exit 1
fi

echo "Resizing files..."

for SIZE in $SIZES
do
  mkdir -p $SIZE
  echo "  $SIZE"
  convert -density $SIZE -background none -interpolate $INTERPOLATION $FILE -interpolative-resize "$SIZE"x png32:"$SIZE/${FILE%.*}.png"
done

for SIZE in $ICOSIZES
do
  ICOFILELIST="$ICOFILELIST $SIZE/${FILE%.*}.png"
done

for SIZE in $PNGSIZES
do
  PNGFILELIST="$PNGFILELIST --raw=$SIZE/${FILE%.*}.png"
done

for SIZE in $MACSIZES
do
  MACFILELIST="$MACFILELIST $SIZE/${FILE%.*}.png"
done

echo "Optimizing..."

for F in */*.png
do
  echo "  $F"
  optipng -nb $F &> /dev/null
done

if [[ ! -e "${FILE%.*}.png" ]]
then
  cp 64/${FILE%.*}.png ./
fi

echo "Creating ICO..."
icotool --create $ICOFILELIST $PNGFILELIST > ${FILE%.*}.ico

echo "Creating ICNS..."
png2icns ${FILE%.*}.icns $MACFILELIST

echo "Creating icon.rc..."
echo "IDI_ICON1 ICON DISCARDABLE \"data/icons/${FILE%.*}.ico\"" > icon.rc

echo "Done!"
