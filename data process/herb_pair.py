#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : herb_pair.py
# @Software: PyCharm

import sys
import numpy as np
import pandas as pd
import pickle
import codecs
from functools import reduce


# get small scale herb pairs
def find_related_pair(herb_ingredient_pair,pd_meridians,data_compound_basic_infor):

    herb_com_related_pairs_all = herb_ingredient_pair[herb_ingredient_pair['herb-id'].isin(pd_meridians['herb-id'])]

    com_data_datframe_all = [data_compound_basic_infor.loc[com, :] for com in
                             herb_com_related_pairs_all['Ingredientid'].tolist()]

    com_data_datframe_all = pd.DataFrame(com_data_datframe_all, columns=data_compound_basic_infor.
                                         columns)
    com_data_datframe_all.insert(0,'herb-id',herb_com_related_pairs_all['herb-id'].tolist())
    com_related = list(set(com_data_datframe_all['Ingredientid'].tolist()))
    herb_related = list(set(herb_com_related_pairs_all['herb-id'].tolist()))
    return com_data_datframe_all,com_related,herb_related


def add_herb_feature(herb_id,herb_ingredient_pair,compound_features_all,feature_names,average_it = True):
    ingre_related = herb_ingredient_pair[herb_ingredient_pair['herb-id']==herb_id]['Ingredientid'].tolist()
    ingre_related_with_structure = [i  for i in ingre_related if i in compound_features_all['Ingredientid']]
    if len(ingre_related_with_structure)!=0:
        data_compound_features_related = compound_features_all.loc[ingre_related_with_structure ,'MW':]
        if average_it == True:
            average_list = data_compound_features_related.mean(axis=0, skipna=True)
            return average_list
        else:
            sum_list = data_compound_features_related.sum(axis=0, skipna=True)
            return sum_list
    else:
        print('no features for herb id',herb_id)
        return ['NA']*len(feature_names)

def add_sorted_column(pd_meridians_herb_with_compound,columns_add):
    dataframe_add = pd_meridians_herb_with_compound.loc[:,columns_add]
    dataframe_add_str = [str(dataframe_add.loc[i,:].tolist()) for i in dataframe_add.index]
    dataframe_add_sorted = [sorted(dataframe_add_str).index(x) for x in dataframe_add_str]
    pd_meridians_herb_with_compound.insert(0, 'sorted', dataframe_add_sorted)
    return pd_meridians_herb_with_compound

def add_compound_class(compound_id,herb_ingredient_pair,pd_herb_meridian_dict,class_names,average_it = True):
    herb_realted = herb_ingredient_pair[herb_ingredient_pair['Ingredientid']==compound_id]['herb-id'].tolist()
    herb_related_with_structure = list(set([i for i in herb_realted if i in pd_herb_meridian_dict.index]))
    if len(herb_related_with_structure) != 0:
        data_herb_class__related = pd_herb_meridian_dict.loc[herb_related_with_structure, :]
        if average_it == True:
            average_list = data_herb_class__related.mean(axis=0, skipna=True)
            return average_list
        else:
            sum_list = data_herb_class__related.sum(axis=0, skipna=True)
            return sum_list
    else:
        print('no features for compound id', compound_id)
        return ['NA'] * len(class_names)


def fill__herb_features(herb_meridian_class,feature_names,herb_ingredient_pair, compound_features_all,
                   average_it = True,sort_herb =True):
    pd_herb_feature = pd.concat([herb_meridian_class,
                                     pd.DataFrame(columns=feature_names)], sort=False)
    # average features for each herb
    pd_herb_feature_add = [add_herb_feature(i, herb_ingredient_pair, compound_features_all,feature_names,average_it)
                                       for i in pd_herb_feature['herb-id'].tolist()]
    # add sorted number to find some row
    pd_herb_feature.loc[:, feature_names] = pd_herb_feature_add
    if sort_herb == True:
        pd_herb_feature_sorted = add_sorted_column(pd_herb_feature, feature_names)
        return pd_herb_feature_sorted
    else:
        return pd_herb_feature

def fill_compound_class(compound_features_related,class_names,herb_ingredient_pair,pd_herb_meridian_dict,feature_names,
                        average_it = True,sort_com = True):
    pd_compound_meridian_class = pd.concat([pd.DataFrame(columns=class_names), compound_features_related
                                            ], sort=False, ignore_index=False)
    # sum class for realted compounds
    pd_com_class_add = [add_compound_class(compound_id, herb_ingredient_pair, pd_herb_meridian_dict, class_names,average_it)
        for compound_id in pd_compound_meridian_class['Ingredientid'].tolist()]
    pd_compound_meridian_class.loc[:, class_names] = pd_com_class_add
    if sort_com == True:
        pd_compound_meridian_class_sorted = add_sorted_column(pd_compound_meridian_class, feature_names)
        return pd_compound_meridian_class_sorted
    else:
        return pd_compound_meridian_class

def find_related_pair_more(herb_ingredient_pair,pd_meridians,data_compound_basic_infor,compound_features_all,adme_names):

    herb_com_related_pairs_all = herb_ingredient_pair[herb_ingredient_pair['herb-id'].isin(pd_meridians['herb-id']) ]
    column_all = data_compound_basic_infor.columns.tolist() + adme_names.tolist()
    com_data_datframe_all = [data_compound_basic_infor.loc[com, :].tolist()+ compound_features_all.loc[com,adme_names].tolist()
                             if com in compound_features_all['Ingredientid'].tolist() else data_compound_basic_infor.loc[com, :].tolist()+
                                                                                           [np.nan]*len(adme_names) for com in
                             herb_com_related_pairs_all['Ingredientid'].tolist() ]

    com_data_datframe_all = pd.DataFrame(com_data_datframe_all, columns = column_all)
    com_data_datframe_all.insert(0,'herb-id',herb_com_related_pairs_all['herb-id'].tolist())
    com_related = list(set(com_data_datframe_all['Ingredientid'].tolist()))
    herb_related = list(set(herb_com_related_pairs_all['herb-id'].tolist()))
    return com_data_datframe_all,com_related,herb_related
