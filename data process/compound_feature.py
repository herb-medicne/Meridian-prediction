#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9.5.2019 13.59
# @Author  : YINYIN
# @Site    : 
# @File    : compound_feature.py
# @Software: PyCharm

import os
import sys
import numpy as np
import pandas as pd
import pickle
import codecs
from functools import reduce
##  deal wirh feature file


def get_related_com_feature(compound_features_all,com_related,need_delete):
    data_compound_features = compound_features_all[compound_features_all['Ingredientid'].isin(com_related)]
    if need_delete == True:
        # delete columns 'ESOL Class' ,'Ali Class', 'Silicos-IT class'
        columns_drop = ['ESOL Class', 'Ali Class','Silicos-IT class','iLOGP','XLOGP3','WLOGP','MLOGP','Silicos-IT',
                        'Log P','iLOGP','XLOGP3','WLOGP','MLOGP','Silicos-IT','Log P',
                        'ESOL Solubility (mg/ml)', 'ESOL Solubility (mol/l)',
                        'Ali Solubility (mg/ml)','Ali Solubility (mol/l)',
                        'Silicos-IT Solubility (mg/ml)',
                        'Silicos-IT Solubility (mol/l)']
        data_compound_features_2 = data_compound_features.drop(columns=  columns_drop)
        # turn factor to '1','0'
        data_compound_features_2 = data_compound_features_2.replace({'No': '0', 'Yes': '1', 'High': '1', 'Low': '0'})
        data_compound_features_2.drop_duplicates(keep='first')
        return data_compound_features_2
    else:
        data_compound_features.drop_duplicates(keep='first')
        return data_compound_features

def compound_eleven_duplicate_feature(compound_features_all):
    compound_features_keep = compound_features_all.drop(columns=['iLOGP','XLOGP3','WLOGP','MLOGP','Silicos-IT',
                                                                   'ESOL Solubility (mg/ml)', 'ESOL Solubility (mol/l)',
                                                                   'Ali Solubility (mg/ml)','Ali Solubility (mol/l)',
                                                                   'Silicos-IT Solubility (mg/ml)',
                                                                   'Silicos-IT Solubility (mol/l)'])
    return compound_features_keep

def compound_delete_seven_feature(compound_features_all):
    compound_features_keep = compound_features_all.drop(columns=['Consensus Log P','ESOL Solubility (mg/ml)',
                                                                 'ESOL Solubility (mol/l)','Ali Solubility (mg/ml)',
                                                                 'Ali Solubility (mol/l)', 'Silicos-IT Solubility (mg/ml)',
                                                                   'Silicos-IT Solubility (mol/l)'])
    return compound_features_keep

def compound_filter_by_property(compound_features_all):
    compound_features_filtered = compound_features_all[(compound_features_all['ESOL Log S']>= -6)&
                                                       (compound_features_all['Ali Log S']>= -6)&
                                                       (compound_features_all['Silicos-IT LogSw'] >= -6)&
                                                       (compound_features_all['GI absorption'] == 1)]
    return compound_features_filtered

def class_label_ingredient(pd_compound_class_sum_sorted_filter,class_name_one):
    delete_ingredients = []
    pd_label = pd.DataFrame(index=pd_compound_class_sum_sorted_filter.index,columns=[class_name_one])
    class_name_one_new = class_name_one+'_delete'
    dict_ingredient = pd_compound_class_sum_sorted_filter.groupby('sorted')['Ingredientid'].apply(list).to_dict()
    dict_ingredient_count = pd_compound_class_sum_sorted_filter.groupby('sorted')['Ingredientid'].apply(list).apply(len).to_dict()
    sorted_mumber_dupli = [i for i,j in dict_ingredient_count.items() if j >1]
    for i in sorted_mumber_dupli:
        ingredients = dict_ingredient[i]
        class_list = pd_compound_class_sum_sorted_filter.loc[ingredients,class_name_one].clip(upper=1)
        if len(set(class_list))!=1:
            delete_ingredients += ingredients
    pd_label.loc[delete_ingredients,class_name_one] = 'delete'
    pd_label = pd_label.fillna('not_delete')
    add_column_list = pd_label[class_name_one].tolist()
    pd_compound_class_sum_sorted_filter.insert(0,class_name_one_new,add_column_list)
    return pd_compound_class_sum_sorted_filter

#list_lung = class_label_ingredient(pd_compound_class_sum_sorted_filter,class_name_one)

def class_label_ingredient_all(pd_compound_class_sum_sorted_filter,class_names):
    for class_name_one in class_names:
        pd_compound_class_sum_sorted_filter = class_label_ingredient(pd_compound_class_sum_sorted_filter, class_name_one)
    return pd_compound_class_sum_sorted_filter

#TODO: def class_label_herb_all()
