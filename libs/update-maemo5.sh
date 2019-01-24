#!/bin/sh
docker run --rm -it --privileged -v /home/dos/git/boiledcorn/utils/libs/maemo5:/libs --entrypoint /bin/bash dosowisko/libsuperderpy-maemo5 -c "cp /scratchbox/users/admin/targets/FREMANTLE_ARMEL/usr/local/lib/* /libs/"
