#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 15.5.2019 16.08
# @Author  : YINYIN
# @Site    : 
# @File    : main.py
# @Software: PyCharm

import os
import sys
import numpy as np
import pandas as pd
import pickle
import codecs
from functools import reduce

os.getcwd()

#1. read data

# compound_basic_infor
data_compound_basic_infor = pd.read_csv('compound_basic_information.csv',encoding="utf-8")
data_compound_basic_infor.index = data_compound_basic_infor['Ingredientid']

# herb baisc information
pd_meridians_with = pd.read_csv('compound_herb_pair.csv',encoding="utf-8")

#herb compound pair
herb_ingredient_pair = pd.read_csv('compound_herb_pair.csv',encoding="utf-8")

#compound feature
import compound_feature
compound_features_all = pd.read_csv('compound_feature.csv')
compound_features_all.index = compound_features_all['Ingredientid']

#2. generate herb meridian matrix

import meridians
herb_meridian_class,wrong_list = meridians.meridian_feature(pd_meridians_with,precessed = True,herb_list_need = None)

#3. generate Herb_Compound pairs detail table

import herb_pair
com_data_datframe_all,com_related,herb_related = herb_pair.find_related_pair(herb_ingredient_pair,
                                                                             herb_meridian_class,data_compound_basic_infor)
import compound_feature
feature_names = compound_features_all.loc[1:2 ,'MW':].columns
adme_names = compound_features_all.loc[1:2 ,'MW':'Synthetic Accessibility'].columns
com_data_datframe_all_more,com_related_more,herb_related_more = herb_pair.find_related_pair_more(herb_ingredient_pair,
                                                                                                 pd_meridians_with,data_compound_basic_infor,
                                                                                                 compound_features_all,adme_names)
com_data_datframe_all.to_csv('Herb_Compound.csv')

#4. generate herb feature matrix

#pd_herb_feature_sum_sorted = herb_pair.fill__herb_features(herb_meridian_class,feature_names,herb_ingredient_pair,
                                                    #compound_features_all, average_it = False,sort_herb =True)
pd_herb_feature_average_sorted = herb_pair.fill__herb_features(herb_meridian_class,feature_names,herb_ingredient_pair,
                                                    compound_features_all, average_it = True,sort_herb =True)

pd_herb_feature_average_sorted.to_csv('herb_feature.csv',encoding="utf-8")

#5. generate compound meridian matrix

pd_herb_meridian_dict = herb_meridian_class.loc[:,'LUNG':'THREE END']
pd_herb_meridian_dict.index = herb_meridian_class['herb-id']
class_names = pd_herb_meridian_dict.columns
common_com_list = [i for i in compound_features_all.index if i in com_related]
compound_features_related = compound_features_all.loc[common_com_list]

pd_compound_class_sum_sorted = herb_pair.fill_compound_class(compound_features_related,class_names,herb_ingredient_pair,
                                                      pd_herb_meridian_dict,feature_names,average_it = False,sort_com = False)
pd_compound_class_sum_sorted.to_csv('compound_meridian.csv')

#6. generate herb feature by filtering compound
compound_features_filtered =  compound_feature.compound_filter_by_property(compound_features_all)

pd_herb_feature_average_filter_sorted  = herb_pair.fill__herb_features(herb_meridian_class,feature_names,herb_ingredient_pair,
                                                                       compound_features_filtered, average_it = True,sort_herb =True)

pd_herb_feature_average_filter_sorted.to_csv('herb_feature_filter_.csv',encoding="utf-8")

