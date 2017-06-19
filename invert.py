# -*- coding: utf-8 -*-
import os, sys
import numpy
from PIL import Image
import PIL.ImageOps

def invertColors(stack):
    new_dir = stack + str('_inverted')
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for fileName in os.listdir(stack) :
        filePath = os.path.join(stack,fileName)
        newImgPath = os.path.join(new_dir,fileName)
        if not os.path.isdir(filePath) and fileName.endswith('.png') :
            with Image.open(filePath) as im:
                inv_img = PIL.ImageOps.invert(im)
                inv_img.save(newImgPath)
    return 0

invertColors('/home/bioprinting/axel/original_data/Thumbnail')
