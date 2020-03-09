#!/bin/sh
docker run --rm -it --privileged -v `realpath maemo5`:/libs --entrypoint /bin/bash dosowisko/libsuperderpy-maemo5 -c "cp -d /scratchbox/users/admin/targets/FREMANTLE_ARMEL/usr/local/lib/* /libs/"
rm maemo5/*.a
