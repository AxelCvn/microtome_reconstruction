# -*- coding: utf-8 -*-
import os, sys

import packages.preprocess as ppp
import packages.conv as conv
import packages.rotation as rot
import packages.ml_alg as ml
# import packages.ml_alg as ml
import time
from natsort import natsorted
import pandas as pd
import csv

def main():
    # #Invert color for the white dataset since the resize fill the background with black color
    # # invertColors('/home/bioprinting/axel/final_data/Thumbnail')
    #
    # # Location of the directory where the data will be (ready to process)
    # finalDataPath = '/home/bioprinting/axel/final_data'
    #
    # #Location of the data before data augmentation and resizing (Original data)
    # curDataPath = '/home/bioprinting/axel/data'
    #
    # # Store the list of the directories in curDataPath
    # stackList = os.listdir(curDataPath)
    # print 'stackList is : ' + str(stackList)
    #
    # # Store the size of the biggest image that will be used to resize all images without loosing information
    # largerSize = ppp.getLargerSize(stackList,curDataPath)
    #
    # # For each stack of the original data, make it png if not (processDir),
    # # Resize it according to the largerSize variable (resize)
    # for stack in os.listdir(curDataPath):
    #     stackPath = os.path.join(curDataPath, stack)
    #     pngStack = ppp.processDir(stackPath)
    #     resizedStack = ppp.resize(pngStack, largerSize, finalDataPath)
    #
    # # Create a flipped stack of each of the stacks in finalDataPath (mirror image = data augmentation)
    # # ppp.flipDataset(finalDataPath)
    #
    #
    # #create lists to store the paths of vectors (data) and rotations (labels)
    # vec_files = []
    # rot_files = []
    #
    # print (os.listdir(finalDataPath))
    # # Update the list of stacks of data according to the final directory and reorder those stacks
    # # to make sure that each is process in a certain order
    # stackList = natsorted(os.listdir(finalDataPath))
    # print 'sorted list : ' + str(stackList)
    #
    #
    #
    # conv_time = time.time()
    # # For each stack rotate all images and save them in directories of pair of images
    # # Save the difference of rotations between pairs of images and save the path of this file in the rotFil
    # # Apply convolution to each image and save the output vector corresponding to a pair of slices, and save the path in vecFile
    # for stack in stackList :
    #     # Create the full path for each stack
    #     stackPath = os.path.join(finalDataPath, stack)
    #     rotFile = rot.create_pairs(stackPath)
    #     print 'RotFile length : ' + str(len(rotFile))
    #     rot_files.append(rotFile)
    #
    #     vecFile = conv.fc(stackPath)
    #     print 'VecFile length : ' + str(len(vecFile))
    #     vec_files.append(vecFile)
    #     print ('vecFile = ' + vecFile)
    #
    # print("--- %s seconds --- TOTAL CONV TIME" % (time.time() - conv_time))


    # List of all vectors representing the output of the convoltion to avoid to have to run the convoltion everytime
    vec_files =  [
        '/home/bioprinting/axel/final_data/Thumbnail_inverted/vecImg.csv',
        '/home/bioprinting/axel/final_data/t2_star_2_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/t2_star_1_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/t2_star_0_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/mouse_kidney_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/kidney_2_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/atlas_0_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/atlas_1_png/vecImg.csv',
        '/home/bioprinting/axel/final_data/Thumbnail_inverted_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/t2_star_2_png_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/t2_star_1_png_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/t2_star_0_png_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/mouse_kidney_png_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/kidney_2_png_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/atlas_0_png_flipped/vecImg.csv',
        '/home/bioprinting/axel/final_data/atlas_1_png_flipped/vecImg.csv'
    ]

    # Same as vectors but for rotations of the slices
    rot_files = [
        '/home/bioprinting/axel/final_data/Thumbnail_inverted/rotations.csv',
        '/home/bioprinting/axel/final_data/t2_star_2_png/rotations.csv',
        '/home/bioprinting/axel/final_data/t2_star_1_png/rotations.csv',
        '/home/bioprinting/axel/final_data/t2_star_0_png/rotations.csv',
        '/home/bioprinting/axel/final_data/mouse_kidney_png/rotations.csv',
        '/home/bioprinting/axel/final_data/kidney_2_png/rotations.csv',
        '/home/bioprinting/axel/final_data/atlas_0_png/rotations.csv',
        '/home/bioprinting/axel/final_data/atlas_1_png/rotations.csv',
        '/home/bioprinting/axel/final_data/Thumbnail_inverted_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/t2_star_2_png_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/t2_star_1_png_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/t2_star_0_png_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/mouse_kidney_png_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/kidney_2_png_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/atlas_0_png_flipped/rotations.csv',
        '/home/bioprinting/axel/final_data/atlas_1_png_flipped/rotations.csv'
    ]

    all_score = []
    nb = 1
    for  i in range(nb):
        print i
        # Arrange the data to make it ready to be the input of the machine learner
        training_data, training_labels, test_data, test_labels = ml.arrange_data(vec_files, rot_files, i)

        # Run the machine learner on the data, learn on training and predict on test data
        res = ml.learn(training_data, training_labels, test_data, test_labels, i)
        all_score.append(res)


    with open('/home/bioprinting/axel/data_res/all_score.csv', "wb") as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerows(all_score)


    # out = open('/home/bioprinting/axel/data_res/all_score_1.csv', "w")
    # for row in all_score:
    #     for column in row:
    #         for val in column :
    #             print val
    #             f.write('%d;' % val)
    #         f.write('\n')


    # rfr_score_df = pd.DataFrame(all_score)
    # rfr_score_df.to_csv('/home/bioprinting/axel/data_res/all_score.csv', index=False, header=False)
    return 0



if __name__ == '__main__':
    main()
