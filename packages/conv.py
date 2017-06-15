import os,sys
import theano
from theano import tensor as T
from theano.tensor.nnet import conv2d
from theano.tensor.signal.pool import pool_2d
import numpy
from PIL import Image
import csv
import pandas as pd
import time
from natsort import natsorted

# theano.config.exception_verbosity='high'
# theano.config.optimizer='None'

##### FROM http://deeplearning.net/tutorial/lenet.html
numpy.set_printoptions(threshold=numpy.inf)

def run_cnn(pairPath):
    #result vector
    flattenImage = []

    # Re order the directory to make sure every images are processed in the desired order
    imgList = natsorted(os.listdir(pairPath))

    # For each image, apply convolution
    for filename in imgList:
        if filename.endswith('.png') :
            filepath = os.path.join(pairPath, filename)

            rng = numpy.random.RandomState(23455)

            # instantiate 4D tensor for input
            input = T.tensor4(name='input')


            ####################################### CONV 1 #######################################
            # initialize shared variable for weights.
            w_shp = (10, 1, 15, 15)
            w_bound = numpy.sqrt(1 * 15 * 15)
            W = theano.shared( numpy.asarray(
                        rng.uniform(
                            low=-1.0 / w_bound,
                            high=1.0 / w_bound,
                            size=w_shp),
                        dtype=input.dtype), name ='W')

            # initialize shared variable for bias (1D tensor) with random values
            # IMPORTANT: biases are usually initialized to zero. However in this
            # particular application, we simply apply the convolutional layer to
            # an image without learning the parameters. We therefore initialize
            # them to random values to "simulate" learning.
            b_shp = (10,)
            b = theano.shared(numpy.asarray(
                        rng.uniform(low=-.5, high=.5, size=b_shp),
                        dtype=input.dtype), name ='b')

            # build symbolic expression that computes the convolution of input with filters in w
            conv_1 = conv2d(input, W)
            ####################################### CONV 1 #######################################

            ####################################### POOL 1 #######################################
            pool_1 = pool_2d(conv_1, (9, 9))
            ####################################### POOL 1 #######################################

            # ####################################### CONV 2 #######################################
            # initialize shared variable for weights.
            w_shp_2 = (10, 10, 15, 15)
            w_bound_2 = numpy.sqrt(10 * 15 * 15)
            W_2 = theano.shared( numpy.asarray(
                        rng.uniform(
                            low=-1.0 / w_bound_2,
                            high=1.0 / w_bound_2,
                            size=w_shp_2),
                        dtype=input.dtype), name ='W')

            # initialize shared variable for bias (1D tensor) with random values
            # IMPORTANT: biases are usually initialized to zero. However in this
            # particular application, we simply apply the convolutional layer to
            # an image without learning the parameters. We therefore initialize
            # them to random values to "simulate" learning.
            b_shp_2 = (10,)
            b_2 = theano.shared(numpy.asarray(
                        rng.uniform(low=-.5, high=.5, size=b_shp_2),
                        dtype=input.dtype), name ='b_2')

            # build symbolic expression that computes the convolution of input with filters in w
            conv_2 = conv2d(pool_1, W_2)

            # ####################################### CONV 2 #######################################

            ####################################### POOL 2 #######################################
            pool_2 = pool_2d(conv_2, (2, 2))

            ####################################### POOL 2 #######################################

            # ####################################### CONV 3 #######################################
            # initialize shared variable for weights.
            w_shp_3 = (10, 10, 5, 5)
            w_bound_3 = numpy.sqrt(10 * 5 * 5)
            W_3 = theano.shared( numpy.asarray(
                        rng.uniform(
                            low=-1.0 / w_bound_3,
                            high=1.0 / w_bound_3,
                            size=w_shp_3),
                        dtype=input.dtype), name ='W')

            # initialize shared variable for bias (1D tensor) with random values
            # IMPORTANT: biases are usually initialized to zero. However in this
            # particular application, we simply apply the convolutional layer to
            # an image without learning the parameters. We therefore initialize
            # them to random values to "simulate" learning.
            b_shp_3 = (10,)
            b_3 = theano.shared(numpy.asarray(
                        rng.uniform(low=-.5, high=.5, size=b_shp_3),
                        dtype=input.dtype), name ='b_3')

            # build symbolic expression that computes the convolution of input with filters in w
            conv_3 = conv2d(pool_2, W_3)

            # ####################################### CONV 3 #######################################

            ####################################### POOL 3 #######################################
            pool_3 = pool_2d(conv_3, (2, 2))

            ####################################### POOL 3 #######################################

            output = T.nnet.sigmoid(pool_3)

            # create theano function to compute filtered images
            f = theano.function([input], output)

            img = Image.open(open(filepath))
            img = numpy.asarray(img.convert('L'), dtype='int64')
            img_size = img.shape[0]

            # put image in 4D tensor of shape (1, 3, height, width)
            img_ = img.reshape(1, 1, img_size, img_size)
            filtered_img = f(img_)*255

            #print filtered_img[0][0]

            # Save the results as a vector
            for i in range(len(filtered_img[0])):
                for j in range(len(filtered_img[0][i])):
                    for k in range(len(filtered_img[0][i][j])):
                        flattenImage.append(filtered_img[0][i][j][k])

    return flattenImage



# Function that call the convolution function
def fc(stack):
    # List to store the results of the convolution of the pair as a vector
    img_vec = []
    for root, dirs, files in os.walk(stack, topdown=True):
        dirs = natsorted(dirs)
        for pair in dirs:
            pair_time = time.time()
            pairPath = os.path.join(stack, pair)
            if len(os.listdir(pairPath))>1 :
                img_vec.append(run_cnn(pairPath))
                print pair + (" Done in --- %s seconds --- (Convolution time))" % (time.time() - pair_time))
            else :
                print 'last dir just one image'

    img_df = pd.DataFrame(img_vec)

    # Save the results in CSV file
    vecFile = os.path.join(stack,'vecImg.csv')
    img_df.to_csv(vecFile, index=False, header=False)

    return vecFile
