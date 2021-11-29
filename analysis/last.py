#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:45:39 2021

@author: bizzy
"""
'''
key

"continent"
"iso_code"

"fully_vaccinated"
"homicide_rate"
"caution"
"total_caeses_per_1million_population"
"recovered_ratio"
"critical_ratio"
'''
import numpy as np
import pandas as pd

import json

def decrease_variable(x):
    return max(x) - x

def normalize(x):
    return (x - min(x)) / (max(x) - min(x))


def SafetyScore(new2):
    a = pd.DataFrame(new2)

    X = np.empty((len(a), 6))
    X[:, 0] = a['total_caeses_per_1million_population']
    X[:, 0] = decrease_variable(X[:, 0])
    X[:, 0] = normalize(X[:, 0])
    #높
    X[:, 1] = a['recovered_ratio']
    X[:, 1] = normalize(X[:, 1])
    
    X[:, 2] = a['critical_ratio']
    X[:, 2] = decrease_variable(X[:, 2])
    X[:, 2] = normalize(X[:, 2])
    #높
    X[:, 3] = a['fully_vaccinated']
    X[:, 3] = normalize(X[:, 3])
    
    X[:, 4] = a['homicide_rate']
    X[:, 4] = decrease_variable(X[:, 4])
    X[:, 4] = normalize(X[:, 4])
    
    X[:, 5] = a['caution']
    X[:, 5] = decrease_variable(X[:, 5])
    X[:, 5] = normalize(X[:, 5])
    
    
    X_cen = X - X.mean(axis=0)  # 평균을 0으로
    X_cov = np.dot(X_cen.T, X_cen) / 59
    
    w, v = np.linalg.eig(X_cov)
    rate = w/w.sum()
    print('explained variance ratio :', w / w.sum())
    
    a['score'] = (rate[0] * X[:, 1]+\
        rate[1] * X[:, 1] +\
        rate[2] * X[:, 2] +\
        rate[3] * X[:, 3] +\
        rate[4] * X[:, 4] +\
        rate[5] * X[:, 5]
    )*100
    return a

with open('./recommend.json', 'r') as f:
    a = json.load(f)