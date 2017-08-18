Download Android SDK, install desired SDK Platform (23 by default, minimum 19). Install build tools, version
24.0.3 or above (except 26.0.0, which is buggy). Download Android NDK.
Set it up according to https://github.com/liballeg/allegro5/blob/master/README_android.txt

Take android-env.example file and fill up everything except stuff like Allegro root, which you don't have yet.

. ./android-env

Dependences that have been tested:
dumb-0.9.3  flac-1.3.2  freetype-2.8  libogg-1.3.2  libtheora-1.1.1  libvorbis-1.3.5  opus-1.2.1  opusfile-0.9  physfs-2.0.3

Freetype can be built without any issues with cmake, while PhysFS needs to be patched to disable CDROM support on Android.
  cmake -DCMAKE_TOOLCHAIN_FILE=$LIBSUPERDERPY_DIR/cmake/android.toolchain ..
  make install

Others are autotools based. For them, get newer config.sub and config.guess from https://git.savannah.gnu.org/gitweb/?p=config.git;a=tree and copy into their trees.
Then you can use:
  ./configure --prefix=$ANDROID_NDK_TOOLCHAIN_ROOT/sysroot/usr --host=arm-linux-androideabi --enable-static --disable-shared --disable-cpplibs --disable-examples --without-allegro CC="arm-linux-androideabi-clang"
  make install

Tip: Install libogg first, so others can be compiled with autodetected OGG support.

Back to Allegro:
  cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DANDROID_TARGET=android-23 -DCMAKE_TOOLCHAIN_FILE=../cmake/Toolchain-android.cmake -DARM_TARGETS="armeabi-v7a" -DWANT_EXAMPLES=no -DWANT_TESTS=no -DWANT_DEMO=no
  make install

Fill the last variables in your android-env file (like path to Allegro build), put it somewhere and point LIBSUPERDERPY_ANDROID_ENV environment variable to it - and you're done.
./package-android.sh (and ./release-android.sh if you have a valid keystore specified in android-env) should work just fine :)
