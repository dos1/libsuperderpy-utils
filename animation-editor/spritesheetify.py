#!/usr/bin/env python

from PIL import Image
from configparser import ConfigParser
from pypacker import sprite_info, sort_images_by_size, pack_images, generate_sprite_sheet
import sys
import uuid

frameCache = []
frameByName = {}

def packFrame(config, id):
    print("Adding frame", id)
    section = 'frame' + str(id)
    frame = config.get(section, 'file', fallback=None)
    sx = config.get(section, 'sx', fallback=None)
    sy = config.get(section, 'sy', fallback=None)
    sw = config.get(section, 'sw', fallback=None)
    sh = config.get(section, 'sh', fallback=None)
    if (sx is not None) or (sy is not None) or (sw is not None) or (sh is not None):
        print("   already spritesheeted")
        return None
    if frame is not None:
        if not frame in frameCache:
            frameCache.append(frame)

def packAnimation(filename):
    print("Spritesheetifying animation " + filename + "...")
    config = ConfigParser()
    config.read(filename)
    frames = config.getint('animation', 'frames')
    for i in range(frames):
        packFrame(config, i)
    #with open(filename, 'w') as configfile:
    #    config.write(configfile)
        
def updateFrame(config, id, spritesheet):
    print("Updating frame", id)
    section = 'frame' + str(id)
    frame = config.get(section, 'file', fallback=None)
    sx = config.get(section, 'sx', fallback=None)
    sy = config.get(section, 'sy', fallback=None)
    sw = config.get(section, 'sw', fallback=None)
    sh = config.get(section, 'sh', fallback=None)
    if (sx is not None) or (sy is not None) or (sw is not None) or (sh is not None):
        print("   already spritesheeted")
        return None
    if frame is not None:
        if not frameByName.get(frame):
            print("   MISSING!")
        else:
            f = frameByName[frame]
            config.set(section, 'file', spritesheet)
            config.set(section, 'origfile', frame)
            config.set(section, 'sx', str(f[1].x + f[0].padding))
            config.set(section, 'sy', str(f[1].y + f[0].padding))
            config.set(section, 'sw', str(f[0].image.size[0]))
            config.set(section, 'sh', str(f[0].image.size[1]))
            frameCache.append(frame)
        
def updateAnimation(filename, spritesheet):
    print("Updating animation " + filename + "...")
    config = ConfigParser()
    config.read(filename)
    frames = config.getint('animation', 'frames')
    for i in range(frames):
        updateFrame(config, i, spritesheet)
    with open(filename, 'w') as configfile:
        config.write(configfile)

for i in range(1, len(sys.argv)):
  packAnimation(sys.argv[i])

for i in range(0, len(frameCache)):
    frameCache[i] = sprite_info(frameCache[i], Image.open(frameCache[i]), 10)

if len(frameCache) > 0:
    images = sort_images_by_size(frameCache)
    packing = pack_images(images, True, ())
    sheet = str(uuid.uuid4()) + ".webp"
    print("Storing the spritesheet to file " + sheet + " ...")

    ss = Image.new('RGBA', (packing.rect.wd, packing.rect.hgt), (0, 0, 0, 0))
    packing.render(ss)
    ss.save(sheet, lossless=True)

    def fillCache(rect):
        for image in rect.children:
            fillCache(image)
        if rect.sprite:
            frameByName[rect.sprite.sprite_name] = (rect.sprite, rect.rect)
    
    fillCache(packing)

    for i in range(1, len(sys.argv)):
        updateAnimation(sys.argv[i], sheet)
else:
    print("nothing to do")
