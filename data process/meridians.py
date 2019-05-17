#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : meridians.py
# @Software: PyCharm

import os
import sys
import numpy as np
import pandas as pd
import pickle
import codecs
from functools import reduce

def meridian_feature(pd_meridians, processed=True, herb_list_need=None):
    # when use herb information down load directly from TCMID database, processed is Flase. 
    # Otherwise, if have chose herbs manually,  processed is True.
    if precessed == False:
        pd_meridians = pd_meridians.loc[:, 'herb-id':'Meridians']
        pd_meridians['Meridians'] = pd_meridians['Meridians'].str.strip()
        # select only herbs with meridian
        pd_meridians_with = pd_meridians[pd_meridians['Meridians'] != 'NA']
        if herb_list_need != None:
            pd_meridians_with = pd_meridians_with.loc[pd_meridians_with['herb-id'].isin(herb_list_need), :]
            meridian_result = meridian_generation(pd_meridians_with, list_meridians)
        else:
            print('no herb_list_need')
            return 0, 0
    else:
        meridian_result = meridian_generation(pd_meridians, list_meridians)
        
    # Get all the herbs that do not have any meridian information
    wrong_herb = meridian_result['herb-id'][meridian_result['LUNG'].isna()].tolist()
    if len(wrong_herb) != 0:
        print('these herb meridian is wrong', wrong_herb)
        print('further check delete or change original data')
        # TODO: check wrong herbs
    return meridian_result, wrong_herb

# all the possible meridians
list_meridians = ['LUNG', 'SPLEEN', 'STOMACH', 'BLADDER', 'CARDIOVASCULAR',
                  'GALLBLADDER', 'HEART', 'KIDNEY', 'LARGE INTESTINE', 'LIVER', 'SMALL INTESTINE', 'THREE END']

# generate meridians matrix. '1' means belonging to specific meridian, '0' means not. 
def meridian_generation(pd_meridians_with, list_meridians):
    pd_meridians_with = pd.concat([pd_meridians_with, pd.DataFrame(columns=list_meridians)], sort=False)
    pd_meridians_with['herb-id'] = pd_meridians_with['herb-id'].fillna(0.0).astype(int)
    # fill the meridian with the '0' and '1' list based on their belonging to the meridian or not
    pd_meridians_with.loc[:, 'LUNG':'THREE END'] = [meridian_list(i, list_meridians)
                                                    for i in pd_meridians_with['Meridians']]
    return pd_meridians_with


# function to turn meridian cell to a fixed length 0 and 1 list.
def meridian_list(meridian_one, list_meridians):
    meridian_related = meridian_one.strip().split(',')
    meridian_related = [i.strip() for i in meridian_related]
    meridian_list_related = [1 if s in meridian_related else 0 for s in list_meridians]
    if sum(meridian_list_related) == len(meridian_related):
        return meridian_list_related
    else:
        [np.nan] * len(list_meridians)

