#!/usr/bin/env python

from PIL import Image
from configparser import ConfigParser
import sys
import os

def readFrame(config, id):
    section = 'frame' + str(id)
    frame = config.get(section, 'file', fallback=None)
    dur = config.get('animation', 'duration', fallback=100)
    framedur = config.get(section, 'duration', fallback=-1)
    quality = config.get('animation', 'quality', fallback=75)
    framequality = config.get(section, 'quality', fallback=-1)
    if framedur != -1:
        dur = framedur
    if framequality != -1:
       quality = framequality
    #if frame[-4:].lower() == ".jpg":
    #    frame = frame[:-3] + "tif"
    #if frame[-4:].lower() == ".png":
    #    frame = frame[:-3] + "tif"
    return "-lossy -q " + str(quality) + " -d " + str(dur) + " \"" + frame + "\" "

def readAnimation(filename):
    filedir = os.path.dirname(filename)
    if filedir:
      os.chdir(filedir)
    config = ConfigParser()
    config.read(os.path.basename(filename))
    frames = config.getint('animation', 'frames')
    cmdline = "img2webp "
    for i in range(frames):
        cmdline = cmdline + readFrame(config, i)
    return cmdline + "-o \"" + os.path.basename(filename[:-3]) + "awebp\""

origdir = os.getcwd()
for i in range(1, len(sys.argv)):
  os.chdir(origdir)
  print("# " + sys.argv[i])
  os.system(readAnimation(sys.argv[i]))
