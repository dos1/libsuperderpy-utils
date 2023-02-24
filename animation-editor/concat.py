#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Only full picture frames are supported for now.

from configparser import ConfigParser
import sys

def exportAnimation(filename):
    config = ConfigParser()
    config.read(filename)
    frames = config.getint('animation', 'frames')
    delay = config.getint('animation', 'duration')
    lines = []
    for i in range(frames):
        section = 'frame' + str(i)
        lines.append("file '" + config.get(section, 'file') + "'")
        lines.append("duration " + str(config.getint(section, 'duration', fallback=delay) / 1000))
    return lines

for i in range(1, len(sys.argv)):
    lines = exportAnimation(sys.argv[i])
    for line in lines:
        print(line)

# Use like: ffmpeg -f concat -i output.txt -vf scale=1920:1080 -x265-params lossless=0 -tag:v hvc1 -c:v libx265 anim.mp4
