#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 14.8.2019 9.58
# @File    : deep_learning_test.py
# @Software: PyCharm

import glob
import scipy.misc
#import matplotlib
#%matplotlib inline
#import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import xlrd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.preprocessing import Binarizer
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix, \
    precision_score, recall_score, f1_score, cohen_kappa_score,roc_auc_score
import math
import os

def get_data(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3333)
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test

def get_datasets(data):
    y= np.array(data.loc[:,['LUNG','SPLEEN','STOMACH','HEART','KIDNEY','LIVER','LARGE INTESTINE']])
    binarizer = Binarizer(0.5).fit(y)
    y_binary = binarizer.transform(y)
    X_ADME = data.loc[:,'MW':'Synthetic Accessibility']
    X_ADME.name = 'ADME'
    X_Ext = data.loc[:,data.columns.str.startswith('ExtFP')]
    X_Ext.name = 'Ext'
    columns_com = X_ADME.columns.tolist() + X_Ext.columns.tolist()
    X_ADME_Ext = data.loc[:, columns_com]
    X_ADME_Ext.name = 'ADME_Ext'
    X_Pubchem = data.loc[:, data.columns.str.startswith('Pubchem')]
    X_Pubchem.name = 'Pubchem'
    X_Sub = data.loc[:, data.columns.str.startswith('SubFP')]
    X_Sub.name = 'Sub'
    X_MACCS = data.loc[:, data.columns.str.startswith('MACCS')]
    X_MACCS.name = 'MACCS'
    X = data.loc[:, 'MW':'SubFP307']
    X.name = 'ADME_all'
    X_list = [X_ADME, X_Ext, X_Pubchem, X_Sub, X_MACCS, X_ADME_Ext, X]
    return X_list, y_binary

# model
def get_model(X_train,y_train):
    x_shape = len(X_train[1])
    dense_shape = int(math.log(x_shape, 2))
    nn = Sequential()
    nn.add(Dense(dense_shape, activation="relu", input_shape=(x_shape,)))
    nn.add(Dropout(0.2))

    nn.add(Dense(dense_shape, activation="relu"))
    nn.add(Dropout(0.2))

    nn.add(Dense(7, activation="sigmoid"))
    nn.compile(optimizer='adam', loss='binary_crossentropy',
     metrics=['accuracy'])
    nn.fit(X_train, y_train,
           batch_size=4,
           epochs=5,
           verbose=1,
           validation_split=0.1)
    return nn

# predict
def predict(nn,X_test,y_test):
    result_pre = nn.predict(X_test)
    meridian_names = ['LUNG','SPLEEN','STOMACH','HEART','KIDNEY','LIVER','LARGE INTESTINE']
    true = pd.DataFrame(y_test, columns = meridian_names)
    result = pd.DataFrame(result_pre, columns = meridian_names)
    return true,result


# evaluate
def evalate(threshhold,meridian,result_data,true_data ):
    meridian_names = ['LUNG', 'SPLEEN', 'STOMACH', 'HEART', 'KIDNEY', 'LIVER', 'LARGE INTESTINE']
    binarizer = Binarizer(threshhold).fit(result_data)
    result_binary = pd.DataFrame(binarizer.transform(result_data),columns=meridian_names)
    eva_scores = list(map(lambda x: x(true_data[meridian], result_binary[meridian]),
                          list_of_functions))
    auc_score = roc_auc_score(true_data[meridian],result_data[meridian] )
    eva_scores.append(auc_score)
    return eva_scores

def meridan_result (threshhold,meridian_names,result_data,true_data):
    pd_add_column_in = ['meridian','tn', 'fp', 'fn', 'tp']
    pd_add_column_in = pd_add_column_in +[fun.__name__ for fun in list_of_functions[1:]]+['auc']

    pd_result = pd.DataFrame()
    for meridian in meridian_names:
        eva_scores = evalate(threshhold, meridian, result_data, true_data)
        eva_scores_falten = list(np.ravel(eva_scores[0])) + eva_scores[1:]
        eva_scores_falten = [meridian] + eva_scores_falten
        pd_result = pd_result.append([eva_scores_falten])

    pd_result.columns = pd_add_column_in
    return pd_result

def filter_result (filter_list,meridian_names,result_data,true_data):
    pd_result = pd.concat(list(map( lambda x: meridan_result(x,meridian_names,result_data,true_data),
                                    filter_list)),keys=filter_list)
    return pd_result

# try different data
def get_model_result_one(X,y):
    X_train, X_test, y_train, y_test = get_data(np.array(X),y)
    nn = get_model(X_train, y_train)
    true,result = predict(nn,X_test,y_test)
    all_result = filter_result(filter_list,meridian_names,result,true)
    return all_result

def get_model_result_all(data):
    X_list,y = get_datasets(data)
    pd_result_all = pd.concat(list(map( lambda x: get_model_result_one(x,y),X_list)),
                              keys= [i.name for i in X_list],axis=0,ignore_index=False)
    return pd_result_all


def model_result_levels(dataset_list):
    pd_all_all = pd.concat(list(map( lambda x:get_model_result_all(x),dataset_list)),
                               keys=[i.name for i in dataset_list], axis=0,sort=True, ignore_index=False)
    return pd_all_all

# apply on my project
meridian_names = ['LUNG','SPLEEN','STOMACH','HEART','KIDNEY','LIVER','LARGE INTESTINE']
list_of_functions = [confusion_matrix,
                     accuracy_score,
                     precision_score,
                     f1_score,
                     recall_score,
                     cohen_kappa_score]
filter_list = [i*0.1 for i in list(range(1,10))]

# prepare data
data_herb = pd.read_csv('herb_before.csv', encoding='utf-8')
data_herb.name = 'Herb'
data_herb_filter = pd.read_csv('herb_filter.csv', encoding='utf-8')
data_herb_filter.name = 'Herb_filter'
data_compound = pd.read_csv('compound.csv', encoding='utf-8')
data_compound = data_compound.dropna()
data_compound.name = 'Compound'
dataset_list = [data_herb,data_herb_filter, data_compound ]

result_all_level = model_result_levels(dataset_list)
herb = get_model_result_all(data_herb)
herb_filter = get_model_result_all(data_herb_filter)
compound_level = get_model_result_all(data_compound)
pd_all_all_seed = pd.concat([herb,herb_filter,compound_level],keys=[i.name for i in dataset_list], axis=0,sort=True, ignore_index=False)
pd_all_all_seed.to_csv('all_result_multi_label.csv')

