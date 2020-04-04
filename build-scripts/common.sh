#!/bin/sh

if [ "`which podman 2> /dev/null`" ]; then
  DOCKER="podman"
  PRIV_DOCKER="sudo podman"
  PRIV_ARGS="--privileged"
else
  DOCKER="docker"
  PRIV_DOCKER="docker"
  PRIV_ARGS="--privileged --userns=host"
fi

if [ "$LIBSUPERDERPY_FORCE_DOCKER" ]; then
  DOCKER="docker"
  PRIV_DOCKER="docker"
  PRIV_ARGS="--privileged --userns=host"
fi

test -t 1 && USE_TTY="-t"
mkdir -p ../.assetcache

