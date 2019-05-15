#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8.5.2019 23.14
# @Author  : YINYIN
# @Site    : 
# @File    : meridians.py
# @Software: PyCharm
import os
import sys
import numpy as np
import pandas as pd
import pickle
import codecs
from functools import reduce

##process_3 : get herb with high quality meridians. delete duplicated. and get herb meridian features
# see othe .py file

def meridian_feature(pd_meridians,precessed = True,herb_list_need = None):
    if precessed == False:
        pd_meridians = pd_meridians.loc[:,'herb-id':'Meridians']
        pd_meridians['Meridians'] = pd_meridians['Meridians'].str.strip()
        #select only herbs with meridian (we select)
        pd_meridians_with = pd_meridians[pd_meridians['Meridians']!='NA']
        if herb_list_need != None:
            pd_meridians_with = pd_meridians_with.loc[pd_meridians_with['herb-id'].isin(herb_list_need),:]
            meridian_result = meridian_generation(pd_meridians_with,list_meridians)
        else:
            print('no herb_list_need')
            return 0,0
    else:
        meridian_result = meridian_generation(pd_meridians,list_meridians)
    # check wrong
    wrong_herb = meridian_result['herb-id'][meridian_result['LUNG'].isna()].tolist()
    if len(wrong_herb) !=0:
        print('these herb meridian is wrong', wrong_herb)
        print('further check delete or change original data')
        # TODO: check herb wrong
    return meridian_result,wrong_herb

list_meridians = ['LUNG', 'SPLEEN', 'STOMACH', 'BLADDER', 'CARDIOVASCULAR',
                      'GALLBLADDER', 'HEART', 'KIDNEY', 'LARGE INTESTINE', 'LIVER', 'SMALL INTESTINE', 'THREE END']
#add new columns about meridians
def meridian_generation(pd_meridians_with,list_meridians):
    pd_meridians_with = pd.concat([pd_meridians_with, pd.DataFrame(columns=list_meridians)],sort=False)
    pd_meridians_with['herb-id'] =  pd_meridians_with['herb-id'].fillna(0.0).astype(int)
    #pd_meridians_with['herb-id'] = map(lambda x:str(x).upper(),pd_meridians_with['herb-id'])
    #pd_meridians_with['herb-id'] = pd.Series(pd_meridians_with['herb-id']).str.upper()
    # fill the meridian with the '0' '1' list based on their belonging to the meridian or not
    pd_meridians_with.loc[:, 'LUNG':'THREE END'] = [meridian_list(i, list_meridians)
                                                    for i in pd_meridians_with['Meridians']]
    return pd_meridians_with

#function to turn meridian list to '0,'1' list
def meridian_list(meridian_one,list_meridians ):
    meridian_related = meridian_one.strip().split(',')
    meridian_related = [i.strip() for i in meridian_related]
    meridian_list_related = [1 if s in meridian_related else 0 for s in list_meridians ]
    if sum(meridian_list_related) == len(meridian_related):
        return meridian_list_related
    else:
        [np.nan] * len(list_meridians)

#exampel:
#pd_meridians_with = pd.read_excel(open('C:\\Users\\yinyin\\Desktop\\herbpair\\20.repeat all on new data\\Herb_Meridian_Compound_Pair_Final_new_2.xlsx','rb'),sheet_name='Herb_Meridian')
#herb_meridian_class,wrong_list = meridian_feature(pd_meridians_with,precessed = True,herb_list_need = None)
