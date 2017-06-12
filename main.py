# -*- coding: utf-8 -*-
import os, sys

import packages.preprocess as ppp
import packages.conv as conv
import packages.rotation as rot
# import packages.ml_alg as ml
import time
from natsort import natsorted

def main():
    # invertColors('/home/bioprinting/axel/final_data/Thumbnail')
    finalDataPath = '/home/bioprinting/axel/final_data'
    curDataPath = '/home/bioprinting/axel/data'
    # stackList = os.listdir(curDataPath)
    # largerSize = ppp.getLargerSize(stackList,curDataPath)
    # for stack in os.listdir(curDataPath):
    #     stackPath = os.path.join(curDataPath, stack)
    #     pngStack = ppp.processDir(stackPath)
    #     resizedStack = ppp.resize(pngStack, largerSize, finalDataPath)
    # ppp.flipDataset(finalDataPath)

    vec_files = []

    rot_files = []

    stackList = natsorted(os.listdir(finalDataPath))

    conv_time = time.time()
    for stack in stackList :
        stackPath = os.path.join(finalDataPath, stack)
        rotFile = rot.create_pairs(stackPath)
        rot_files.append(rotFile)

        vecFile = conv.fc(stackPath)
        vec_files.append(vecFile)
        print ('vecFile = ' + vecFile)

    print("--- %s seconds --- TOTAL CONV TIME" % (time.time() - conv_time))

    # vec_files =  [
    #     '/home/bioprinting/axel/final_data/Thumbnail_inverted/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_2_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_1_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_0_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/mouse_kidney_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/kidney_2_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/atlas_0_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/atlas_1_png/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/Thumbnail_inverted_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_2_png_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_1_png_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_0_png_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/mouse_kidney_png_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/kidney_2_png_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/atlas_0_png_flipped/vecImg.csv',
    #     '/home/bioprinting/axel/final_data/atlas_1_png_flipped/vecImg.csv'
    # ]
    #
    # rot_files = [
    #     '/home/bioprinting/axel/final_data/Thumbnail_inverted/rotations.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_2_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_1_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_0_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/mouse_kidney_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/kidney_2_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/atlas_0_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/atlas_1_png/rotations.csv',
    #     '/home/bioprinting/axel/final_data/Thumbnail_inverted_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_2_png_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_1_png_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/t2_star_0_png_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/mouse_kidney_png_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/kidney_2_png_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/atlas_0_png_flipped/rotations.csv',
    #     '/home/bioprinting/axel/final_data/atlas_1_png_flipped/rotations.csv'
    # ]

    training_data, training_labels, test_data, test_labels = ml.arrange_data(vec_files, rot_files)
    res = ml.learn(training_data, training_labels, test_data, test_labels)

    return 0

if __name__ == '__main__':
    main()
