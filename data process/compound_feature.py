#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : compound_feature.py
# @Software: PyCharm

import os
import sys
import numpy as np
import pandas as pd
import pickle
import codecs
from functools import reduce

# if you use the adme from SwissADME data base, some pre-process have to done. 
def get_related_com_feature(compound_features_all,com_related,need_delete):
    # only select the compound related
    data_compound_features = compound_features_all[compound_features_all['Ingredientid'].isin(com_related)]
    # decide how many feature to use. Whether the useless column has been delete manully. If not, select.
    if need_delete == True:
        # delete columns useless
        columns_drop = ['ESOL Class', 'Ali Class','Silicos-IT class','Consensus Log P',
                        'ESOL Solubility (mg/ml)', 'ESOL Solubility (mol/l)',
                        'Ali Solubility (mg/ml)','Ali Solubility (mol/l)',
                        'Silicos-IT Solubility (mg/ml)',
                        'Silicos-IT Solubility (mol/l)']
        data_compound_features_2 = data_compound_features.drop(columns=  columns_drop)
        # make character to number for better modelling
        data_compound_features_2 = data_compound_features_2.replace({'No': '0', 'Yes': '1', 'High': '1', 'Low': '0'})
        # remove duplicate columns
        data_compound_features_2.drop_duplicates(keep='first')
        return data_compound_features_2
    else:
        data_compound_features.drop_duplicates(keep='first')
        return data_compound_features

# delete seven useless column
def compound_delete_seven_feature(compound_features_all):
    compound_features_keep = compound_features_all.drop(columns=['Consensus Log P','ESOL Solubility (mg/ml)',
                                                                 'ESOL Solubility (mol/l)','Ali Solubility (mg/ml)',
                                                                 'Ali Solubility (mol/l)', 'Silicos-IT Solubility (mg/ml)',
                                                                   'Silicos-IT Solubility (mol/l)'])
    return compound_features_keep

# do compound filtering based on solubility and GI absorption as described in our article
def compound_filter_by_property(compound_features_all):
    compound_features_filtered = compound_features_all[(compound_features_all['ESOL Log S']>= -6)&
                                                       (compound_features_all['Ali Log S']>= -6)&
                                                       (compound_features_all['Silicos-IT LogSw'] >= -6)&
                                                       (compound_features_all['GI absorption'] == 1)]
    return compound_features_filtered

