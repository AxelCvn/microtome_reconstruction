# -*- coding: utf-8 -*-
import os, sys
import numpy
from PIL import Image
import pandas as pd
# import PIL.ImageOps
from natsort import natsorted
import glob

def organizePredictions(pred_file):
    list_rot = []
    # for rotPair in pred_file :
    tmpList = pd.read_csv(pred_file, header=None)
    for index, row in tmpList.iterrows():
        list_rot.append(row.tolist()[0])
    print list_rot
    final_rot = [0]
    for i in range(0,len(list_rot)):
        final_rot.append(final_rot[i]-list_rot[i])
    print final_rot
    return final_rot

def applyPredRot(directory, final_pred):
    pre, end = os.path.split(directory)
    end = end + '_corrected'
    new_dir = os.path.join(directory,end)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    #For each image of the stack, create a png copy and save it in the new directory
    stackPNG = os.path.join(directory, '*.png')
    orderedDir  = natsorted(glob.glob(stackPNG))
    print len(orderedDir)
    for i in range(0,len(orderedDir)-3) :
        # print i
        imgPath = orderedDir[i]
        # print imgPath
        pre, end = os.path.split(imgPath)
        imPath = 'corrected_' + end
        # print imPath
        corImgPath = os.path.join(new_dir,imPath)
        if not os.path.isdir(imgPath) and (imgPath.endswith('.png')):
            with Image.open(imgPath) as im:
                angle = final_pred[i]
                correctedIm = im.rotate(angle)
                correctedIm.save(corImgPath)
    return new_dir

def main(p_file, dir):
    rot = organizePredictions(p_file)
    applyPredRot(dir, rot)
    return 0

pred_file = '/home/bioprinting/axel/data_res/rfr_pred_100.csv'
dir_stack = '/home/bioprinting/axel/rotated_data/atlas_1_png_rotated'

if __name__ == '__main__':
 main(pred_file, dir_stack)
