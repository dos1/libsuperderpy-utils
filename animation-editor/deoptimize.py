#!/usr/bin/env python

from PIL import Image
from configparser import ConfigParser
import sys

frameCache = {}

def uncropImage(filename, x, y, w, h):
    image = Image.open(filename)
    newimage = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    newimage.paste(image, (x, y))
    newimage.save(filename, lossless=True)
    frameCache[filename] = True

def uncropFrame(config, id):
    print("Uncropping frame", id)
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
        print("   spritesheeted; not uncropping")
        return None
    if (frame is not None) and (x is not None) and (y is not None):
        if frameCache.get(frame):
            print("   already uncropped", frame)
            config.remove_option(section, 'x')
            config.remove_option(section, 'y')
            return frameCache[frame]
        else:
            uncropImage(frame, int(x), int(y), int(w), int(h))
            print("  ", frame)
            config.remove_option(section, 'x')
            config.remove_option(section, 'y')

def uncropAnimation(filename):
    print("Deoptimizing animation " + filename + "...")
    config = ConfigParser()
    config.read(filename)
    frames = config.getint('animation', 'frames')
    for i in range(frames):
        uncropFrame(config, i)
    with open(filename, 'w') as configfile:
        config.write(configfile)

for i in range(1, len(sys.argv)):
  uncropAnimation(sys.argv[i])
