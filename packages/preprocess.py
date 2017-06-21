# -*- coding: utf-8 -*-
import os, sys
import numpy
from PIL import Image
import shutil
from math import *
import glob
import csv
import PIL.ImageOps

#Check if first file of a directory is tif or not and depending on it convert to png
def processDir(stackPath) :
    print (stackPath)

    #
    for root, dirs, files in os.walk(stackPath, topdown=True):
        for name in files:
            #print name
            if name.endswith('tif'):
                print ('TEST')
                stackIsTif = True
                break
            else :
                # print 'File tested : ' + str(name)
                stackIsTif = False
                break
        break

    #If stackIsTif convert to PNG
    if stackIsTif :
        print"Let's convert stack to PNG"
        stackPath = tifToPng(stackPath)
    else :
        print"We can now resize the stack"
        #stackPath = os.path.join(stackPath, 'png')
        print stackPath
    return stackPath

#Create a png copy of images of a stack and return the path of the new stack
def tifToPng(directory):
    print" Working in : " + directory + " directory"
    #Create new directory to store the new png images
    pre, end = os.path.split(directory)
    end = end + '_png'
    new_dir = os.path.join(directory,end)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    #For each image of the stack, create a png copy and save it in the new directory
    for fileName in os.listdir(directory) :
        imgPath = os.path.join(directory,fileName)
        if not os.path.isdir(imgPath) and (imgPath.endswith('.tif')):
            with Image.open(imgPath) as im:
                finalPath = os.path.join(new_dir,fileName)
                pre, ext = os.path.splitext(finalPath)
                finalPath = finalPath = pre + '.png'
                im.mode='I'
                im.point(lambda i:i*(1./256)).convert('L').save(finalPath)
        else :
            filePath = os.path.join(directory,fileName)
    return new_dir

# Resize the stack such as rotations don't crop the original image
def resize(stackPath, largerSize, newDir):
    #First check if stack is already resized
    #The stack path is supposed to only contain images (as files)
    for root, dirs, files in os.walk(stackPath, topdown=True):
        for name in files:
            testPath = os.path.join(stackPath,name)
            pre, ext = os.path.splitext(testPath)
            if pre.endswith('resized'):
                resized = True
                break
            else :
                resized = False
                break
        break

    if not resized :
        print'Start resizing stack'
        #Create a new directory to store resized images
        baseDir, curDir = os.path.split(stackPath)
        print curDir
        new_dir = os.path.join(newDir,curDir)
        print 'New Dir = ' + str(new_dir)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        #Resize each image and save it in the new directory
        for fileName in os.listdir(stackPath) :
            filePath = os.path.join(stackPath,fileName)
            if not os.path.isdir(filePath) and fileName.endswith('.png') :
                with Image.open(filePath) as im:

                    diago = int(round(sqrt(2)*largerSize))
                    new_size = (diago,diago)

                    new_im = Image.new("L", new_size)
                    new_im.paste(im,((new_size[0]-im.size[0])/2,(new_size[1]-im.size[1])/2))

                    newFileName = os.path.join(new_dir,fileName)
                    pre, ext = os.path.splitext(newFileName)
                    newFileName = pre + '_resized' + ext
                    new_im.save(newFileName)

            else :
                print" WARNING " +str(filePath) + " does not exist or is not a png image !!"
        print 'Ready to rotate'
        return new_dir
    else :
        print'This stack is already resized, we can rotate it'
        return stackPath

def flipDataset(dataset):
    for root, dirs, files in os.walk(dataset, topdown=True):
        for stacks in dirs :
            cur_stack = os.path.join(dataset,stacks)
            if not cur_stack.endswith('_flipped'):
                new_stack = cur_stack + '_flipped'
                if not os.path.exists(new_stack):
                    os.mkdir(new_stack)
                print new_stack
                for img in os.listdir(cur_stack) :
                    imgPath = os.path.join(cur_stack, img)
                    if not os.path.isdir(imgPath) and img.endswith('.png') :
                        newImgPath = os.path.join(new_stack, img)
                        with Image.open(imgPath) as im :
                            new_im = im.transpose(Image.FLIP_LEFT_RIGHT)
                            new_im.save(newImgPath)
            else :
                pass
    return 0

#Check all stacks and get the larger size of image to resize other stacks
def getLargerSize(stacks, basePath):
    largerSize = 0
    for stack in stacks:
        stack = os.path.join(basePath, stack)
        for root, dirs, files in os.walk(stack, topdown=True):
            print 'PASS IN LOOP'
            for name in files:
                print name
                imgPath = os.path.join(stack, name)
                with Image.open(imgPath) as im:
                    if im.size[0] > im.size[1] :
                        if im.size[0] > largerSize :
                            largerSize = im.size[0]
                            break
                        else :
                            break
                    else :
                        if im.size[1] > largerSize :
                            largerSize = im.size[1]
                            break
                        else :
                            break
            break

    return largerSize
