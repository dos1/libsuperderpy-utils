#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from configparser import ConfigParser
import sys
from crop import cropImage

frameCache = {}

def cropFrame(config, id):
    print("Cropping frame", id)
    section = 'frame' + str(id)
    frame = config.get(section, 'file', fallback=None)
    x = config.get(section, 'x', fallback=None)
    y = config.get(section, 'y', fallback=None)
    w = config.get('animation', 'width', fallback=-1)
    h = config.get('animation', 'height', fallback=-1)
    sx = config.get(section, 'sx', fallback=None)
    sy = config.get(section, 'sy', fallback=None)
    sw = config.get(section, 'sw', fallback=None)
    sh = config.get(section, 'sh', fallback=None)
    if (sx is not None) or (sy is not None) or (sw is not None) or (sh is not None):
        print("   spritesheeted; not cropping")
        return None
    if (frame is not None) and (x is None) and (y is None):
        if frameCache.get(frame):
            print("   from cache", frame, frameCache[frame])
            config.set(section, 'x', str(frameCache[frame][0]))
            config.set(section, 'y', str(frameCache[frame][1]))
            return frameCache[frame]
        else:
            box = cropImage(frame)
            frameCache[filename] = box
            print("  ", frame, box[0], box[1])
            config.set(section, 'x', str(box[0]))
            config.set(section, 'y', str(box[1]))
            return box
    else:
        if frame is not None:
            image = Image.open(frame)
            frameCache[frame] = (int(x), int(y), image.width, image.height, int(w), int(h))
            return frameCache[frame]
    return None

def cropAnimation(filename):
    print("Optimizing animation " + filename + "...")
    config = ConfigParser()
    config.read(filename)
    frames = config.getint('animation', 'frames')
    w = -1
    h = -1
    for i in range(frames):
        box = cropFrame(config, i)
        if box:
            w = max(box[4], w)
            h = max(box[5], h)
    if w > -1 and h > -1:
        print("...done. Size: " + str(w) + "x" + str(h))
        config.set('animation', 'width', str(w))
        config.set('animation', 'height', str(h))
    with open(filename, 'w') as configfile:
        config.write(configfile)

for i in range(1, len(sys.argv)):
  cropAnimation(sys.argv[i])
