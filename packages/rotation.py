# -*- coding: utf-8 -*-
import os, sys
import numpy
from PIL import Image
import shutil
from math import *
import glob
import csv
import pandas as pd

def create_pairs(stack):
    pre, end = os.path.split(stack)
    end = end + '_rotated'
    rot_dir = os.path.join('/home/bioprinting/axel/rotated_data',end)
    if not os.path.exists(rot_dir):
        os.mkdir(rot_dir)

    print ' Start creating rotated pairs'
    i=0
    # angleSign = 1
    stackPNG = os.path.join(stack, '*.png')
    filesList = sorted(glob.glob(stackPNG))
    randomArray = numpy.random.uniform(0,720,len(filesList))
    #print randomArray
    rotations = []
    new_dir = os.path.join(stack,str(i))
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for pic in filesList :
        base, ext = os.path.splitext(pic)
        pre_0, end_0 = os.path.split(base)
        end_0 = end_0 + '.png'
        rotImgPath = os.path.join(rot_dir,end_0)
        if i==0 :
            with Image.open(pic) as im :
                ext = str(i)+'.png'
                newImgPath = os.path.join(new_dir,ext)
                #print newImgPath
                r = randomArray[i]
                angle = (-30)+(60*r/720)
                #print angle
                newImg = im.rotate(angle)
                newImg.save(newImgPath)
                newImg.save(rotImgPath)
                rotations.append(angle)
        else :
            prev_dir = new_dir
            new_dir = os.path.join(stack,str(i))
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            with Image.open(pic) as im :
                ext = str(i)+'.png'
                newImgPath = os.path.join(new_dir,ext)
                newImgPrevPath = os.path.join(prev_dir,ext)
                print newImgPath
                r = randomArray[i]
                angle = (-30)+(60*r/720)
                #print angle
                newImg = im.rotate(angle)
                newImg.save(newImgPath)
                newImg.save(newImgPrevPath)
                newImg.save(rotImgPath)
                rotations.append(angle)
        i+=1
    pairsRot = []
    for j in range(1,len(rotations)):
        rot = rotations[j]-rotations[j-1]
        pairsRot.append(rot)
    #print pairsRot
    rotFile = os.path.join(stack,'rotations.csv')
    pairsRotDf = pd.DataFrame(pairsRot)
    pairsRotDf.to_csv(rotFile, index=False, header=False)

    return rotFile
