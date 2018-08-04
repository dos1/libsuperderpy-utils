#!/usr/bin/env python

from PIL import Image
from configparser import ConfigParser
import sys

frameCache = {}

def cropImage(filename):
    image = Image.open(filename)
    imageBox = image.convert("RGBa").getbbox()
    if not imageBox:
        imageBox = (0, 0, 1, 1)
    image.crop(imageBox).save(filename, lossless=True)
    frameCache[filename] = imageBox
    return imageBox

def cropFrame(config, id):
    print("Cropping frame", id)
    section = 'frame' + str(id)
    frame = config.get(section, 'file', fallback=None)
    x = config.get(section, 'x', fallback=None)
    y = config.get(section, 'y', fallback=None)
    w = config.get('animation', 'width', fallback=-1)
    h = config.get('animation', 'height', fallback=-1)
    if (frame is not None) and (x is None) and (y is None):
        if frameCache.get(frame):
            print("   from cache", frame, frameCache[frame])
            config.set(section, 'x', str(frameCache[frame][0]))
            config.set(section, 'y', str(frameCache[frame][1]))
            return frameCache[frame]
        else:
            box = cropImage(frame)
            print("  ", frame, box[0], box[1])
            config.set(section, 'x', str(box[0]))
            config.set(section, 'y', str(box[1]))
            return box
    else:
        if frame is not None:
            frameCache[frame] = (x, y, w, h)
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
            w = max(box[2], w)
            h = max(box[3], h)
    if w > -1 and h > -1:
        config.set('animation', 'width', str(w))
        config.set('animation', 'height', str(h))
    with open(filename, 'w') as configfile:
        config.write(configfile)

for i in range(1, len(sys.argv)):
  cropAnimation(sys.argv[i])
