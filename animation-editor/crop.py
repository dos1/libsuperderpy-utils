#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import sys

def cropImage(filename):
    image = Image.open(filename)
    imageBox = image.convert("RGBa").getbbox()
    w, h = image.width, image.height
    if not imageBox:
        imageBox = (0, 0, 1, 1, w, h)
    image.crop(imageBox).save(filename, lossless=True)
    return (imageBox[0], imageBox[1], imageBox[2], imageBox[3], w, h)

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        box = cropImage(sys.argv[i])
        print(box)
