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


# get the related compounds of herbs we need according herb compound pairs relationship
def find_related_pair(herb_ingredient_pair, pd_meridians, data_compound_basic_infor):
    herb_com_related_pairs_all = herb_ingredient_pair[herb_ingredient_pair['herb-id'].isin(pd_meridians['herb-id'])]
    #construction the table of herb-compound-pair details in our Supplementray table 1.
    com_data_datframe_all = [data_compound_basic_infor.loc[com, :] for com in
                             herb_com_related_pairs_all['Ingredientid'].tolist()]
    com_data_datframe_all = pd.DataFrame(com_data_datframe_all, columns=data_compound_basic_infor.
                                         columns)
    com_data_datframe_all.insert(0, 'herb-id', herb_com_related_pairs_all['herb-id'].tolist())
    # get a list about all related herbs
    com_related = list(set(com_data_datframe_all['Ingredientid'].tolist()))
    # get a list about all related compound 
    herb_related = list(set(herb_com_related_pairs_all['herb-id'].tolist()))
    return com_data_datframe_all, com_related, herb_related

# function of calculating the feature for one herb
def add_herb_feature(herb_id, herb_ingredient_pair, compound_features_all, feature_names, average_it=True):
    # get the related ingredients of this herb based on herb id 
    ingre_related = herb_ingredient_pair[herb_ingredient_pair['herb-id'] == herb_id]['Ingredientid'].tolist()
    # get the ingredients with compound features
    ingre_related_with_structure = [i for i in ingre_related if i in compound_features_all['Ingredientid']]
    # if got at least one ingredients, continue. otherwise, if not got any ingredients,fill with all 'NA'.  
    if len(ingre_related_with_structure) != 0:
        # get all the related compound features rows
        data_compound_features_related = compound_features_all.loc[ingre_related_with_structure, 'MW':]
        # if we want average value of each kind of feature,average_it == True. Otherwise, calculate sum value.
        if average_it == True:
            average_list = data_compound_features_related.mean(axis=0, skipna=True)
            return average_list
        else:
            sum_list = data_compound_features_related.sum(axis=0, skipna=True)
            return sum_list
    else:
        print('no features for herb id', herb_id)
        return ['NA'] * len(feature_names)

# based on herb meridians classification to calculate meridian value for one compound
def add_compound_class(compound_id, herb_ingredient_pair, pd_herb_meridian_dict, class_names, average_it=True):
    # get the related herbs on this compounds
    herb_realted = herb_ingredient_pair[herb_ingredient_pair['Ingredientid'] == compound_id]['herb-id'].tolist()
    # get the herb that with meridians information
    herb_related_with_structure = list(set([i for i in herb_realted if i in pd_herb_meridian_dict.index]))
    # if at least one herb targeted, continue. Otherwise, fill the meridian as all 'na'
    if len(herb_related_with_structure) != 0:
        # get all the meridians rows about related herbs
        data_herb_class__related = pd_herb_meridian_dict.loc[herb_related_with_structure, :]
        # decide get average value or sum value
        if average_it == True:
            average_list = data_herb_class__related.mean(axis=0, skipna=True)
            return average_list
        else:
            sum_list = data_herb_class__related.sum(axis=0, skipna=True)
            return sum_list
    else:
        print('no features for compound id', compound_id)
        return ['NA'] * len(class_names)

# get the features for all the herbs
def fill__herb_features(herb_meridian_class, feature_names, herb_ingredient_pair, compound_features_all,
                        average_it=True):
    pd_herb_feature = pd.concat([herb_meridian_class,
                                 pd.DataFrame(columns=feature_names)])
    # average features for each herb
    pd_herb_feature_add = [add_herb_feature(i, herb_ingredient_pair, compound_features_all, feature_names, average_it)
                           for i in pd_herb_feature['herb-id'].tolist()]
    pd_herb_feature.loc[:, feature_names] = pd_herb_feature_add
    return pd_herb_feature

# get the meridians for all the compounds
def fill_compound_class(compound_features_related, class_names, herb_ingredient_pair, pd_herb_meridian_dict,
                        feature_names,
                        average_it=True):
    pd_compound_meridian_class = pd.concat([pd.DataFrame(columns=class_names), compound_features_related
                                            ], sort=False)
    # get meridian classification for realted compounds
    pd_com_class_add = [
        add_compound_class(compound_id, herb_ingredient_pair, pd_herb_meridian_dict, class_names, average_it)
        for compound_id in pd_compound_meridian_class['Ingredientid'].tolist()]
    pd_compound_meridian_class.loc[:, class_names] = pd_com_class_add
    return pd_compound_meridian_class

# add ADME information
def find_related_pair_more(herb_ingredient_pair, pd_meridians, data_compound_basic_infor, compound_features_all,
                           adme_names):
    herb_com_related_pairs_all = herb_ingredient_pair[herb_ingredient_pair['herb-id'].isin(pd_meridians['herb-id'])]
    column_all = data_compound_basic_infor.columns.tolist() + adme_names.tolist()
    com_data_datframe_all = [
        data_compound_basic_infor.loc[com, :].tolist() + compound_features_all.loc[com, adme_names].tolist()
        if com in compound_features_all['Ingredientid'].tolist() else data_compound_basic_infor.loc[com, :].tolist() +
                                                                      [np.nan] * len(adme_names) for com in
        herb_com_related_pairs_all['Ingredientid'].tolist()]

    com_data_datframe_all = pd.DataFrame(com_data_datframe_all, columns=column_all)
    com_data_datframe_all.insert(0, 'herb-id', herb_com_related_pairs_all['herb-id'].tolist())
    com_related = list(set(com_data_datframe_all['Ingredientid'].tolist()))
    herb_related = list(set(herb_com_related_pairs_all['herb-id'].tolist()))
    return com_data_datframe_all, com_related, herb_related
