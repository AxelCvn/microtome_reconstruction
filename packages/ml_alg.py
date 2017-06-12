import numpy as np
import random
from sklearn import random_projection
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn import neural_network
import csv
import os
import time
import ast
import matplotlib.pyplot as plt
import pandas as pd

def arrange_data(vec_files, rot_files):
    dataNb = len(vec_files)

    test_datasetNb = random.randint(0,dataNb-1)

    training_data = []
    test_data = []

    i = 0
    for i in range(dataNb):
        if not i == test_datasetNb :
            tmpList = pd.read_csv(vec_files[i],header=0)
                for index, row in tmpList.iterrows():
                    training_set.append(row.tolist())
        else :
            tmpList = pd.read_csv(vec_files[i],header=0)
                for index, row in tmpList.iterrows():
                    test_set.append(row.tolist())


    training_labels = []
    test_labels = []

    j = 0
    for j in range(dataNb):
        if not j == test_datasetNb :
            tmpList = pd.read_csv(rot_files[j],header=0)
                for index, row in tmpList.iterrows():
                    training_set.append(row.tolist())
        else :
            tmpList = pd.read_csv(rot_files[j],header=0)
                for index, row in tmpList.iterrows():
                    test_set.append(row.tolist())

    test_pred_df = pd.DataFrame(test_labels)
    test_pred_df.to_csv('/home/bioprinting/axel/data_res/pred_val.csv', index=False, header=False)
    
    return training_data, training_labels, test_data, test_labels

def learn(training_data, training_labels, test_data, test_labels):
    ##################### SUPPORT VECTOR REGRESSION #####################
    svr_res_lin = []
    svr_res_poly =[]

    #svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_lin = svm.SVR(kernel='linear', C=1e3)
    svr_poly = svm.SVR(kernel='poly', C=1e3, degree=2)

    #y_rbf = svr_rbf.fit(inputDataTest, inputMetaDataTest)

    lin_Time = time.time()
    y_lin = svr_lin.fit(training_data, training_labels)
    print("--- %s seconds --- Linear training Time" % (time.time() - lin_Time))
    poly_Time = time.time()
    y_poly = svr_poly.fit(training_data, training_labels)
    print("--- %s seconds --- Poly training Time" % (time.time() - poly_Time))
    ################## TRAINING DATA ##################
    svr_linTrain = y_lin.score(training_data, training_labels)
    svr_polyTrain = y_poly.score(training_data, training_labels)
    print "svr_linTrain = " + str(svr_linTrain)
    print "svr_polyTrain = " + str(svr_polyTrain)


    #################### TEST DATA ####################
    #LINEAR SVR
    svr_lin = y_lin.score(test_data, test_labels)
    print "svr_linTest = " + str(svr_lin)
    svr_res_lin.append(svr_lin)

    #POLY SVR
    svr_poly = y_poly.score(test_data, test_labels)
    print "svr_polyTest = " + str(svr_poly)
    svr_res_poly.append(svr_poly)

    ############ MAKE AND SAVE PREDICTION ############
    lin_pred = y_lin.predict(test_data)
    poly_pred = y_poly.predict(test_data)

    lin_err = 0
    for z in range(len(test_labels)):
        lin_err += abs(lin_pred[z]-test_labels[z])
    lin_err = lin_err/len(test_labels)
    print ' Linear SVR error : ' + str(lin_err)

    poly_err = 0
    for z in range(len(test_labels)):
        poly_err += abs(poly_pred[z]-test_labels[z])
    poly_err = poly_err/len(test_labels)
    print ' Poly SVR error : ' + str(poly_err)

    lin_pred_df = pd.DataFrame(lin_pred)
    poly_pred_df = pd.DataFrame(poly_pred)

    lin_pred_df.to_csv('/home//lin_pred.csv', index=False, header=False)
    poly_pred_df.to_csv('/home/bioprinting/axel/data_res/poly_pred.csv', index=False, header=False)

    ###################### RANDOM FOREST REGRESSOR ######################
    rfr_res=[]
    rfr_iter = []
    rfr_iter_val = []
    x = [10, 50, 100]
    for j in x :

        nb_estim = j
        # RandomForestRegressor
        rgs = RandomForestRegressor(n_estimators=nb_estim)

        forestTime = time.time()
        rgs = rgs.fit(training_data, training_labels)
        print("--- %s seconds --- RFR Training Time with %d estimators" %((time.time() - forestTime),j))

        resTrain = rgs.score(training_data, training_labels)
        print "TRAIN results with RandomForestRegressor : " + str(resTrain)

        print "estimators :" + str(nb_estim)
        res = rgs.score(test_data, test_labels)
        rfr_iter.append(res)
        print "TEST results with RandomForestRegressor : " + str(res)

        rfr_pred = rgs.predict(test_data)

        rfr_pred_df = pd.DataFrame(rfr_pred)

        rfr_pred_path = '/home/bioprinting/axel/data_res/rfr_pred_' + str(j) + '.csv'

        rfr_pred_df.to_csv(rfr_pred_path, index=False, header=False)

        rfr_err = 0
        for z in range(len(test_labels)):
            rfr_err += abs(rfr_pred[z]-test_labels[z])
        rfr_err = rfr_err/len(test_labels)
        print ' RFR error : ' + str(rfr_err) + 'With ' + str(j) + 'estimators'

    rfr_res.append(rfr_iter)
    # rfr_val.append(rfr_iter_val)
    #####################################################################

    ##################### NEURAL NETWORK REGRESSION #####################
    hd_lrs = [100,200,300]

    nnr_res =[]
    nnr_iter = []
    for h in hd_lrs :

        nnr = neural_network.MLPRegressor(hidden_layer_sizes=h,activation='identity',solver='adam')

        NNRTime = time.time()
        nnr = nnr.fit(training_data, training_labels)
        print("--- %s seconds --- NNR Training Time with %d estimators" %((time.time() - NNRTime),h))

        resVal = nnr.score(training_data, training_labels)

        print "TRAIN results with NeuralNetworkRegressor : " + str(resVal)
        res = nnr.score(test_data, test_labels)

        nnr_pred = nnr.predict(test_data)

        nnr_pred_df = pd.DataFrame(nnr_pred)

        nnr_pred_path = '/home/bioprinting/axel/data_res/nnr_pred_' + str(h) + '.csv'

        rfr_pred_df.to_csv(rfr_pred_path, index=False, header=False)

        print "TEST results with NeuralNetworkRegressor : " + str(res)
        nnr_iter.append(res)

        nnr_err = 0
        for z in range(len(test_labels)):
            nnr_err += abs(nnr_pred[z]-test_labels[z])
        nnr_err = nnr_err/len(test_labels)
        print ' NNR error : ' + str(nnr_err) + 'With hidden layers of size :' + str(h)

    nnr_res.append(nnr_iter)

    return 0
