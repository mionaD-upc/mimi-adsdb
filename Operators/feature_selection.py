from sklearn.model_selection import train_test_split
import sys

import utils 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Transformation
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import power_transform
from sklearn.pipeline import Pipeline
# Feature Selection
import sklearn_relief as sr
# Models
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def feature_selection(path):
    data = utils.DBtable_to_df(f'{path}/integration.duckdb', 'sandbox')
    dataN = data.drop(columns=['Year','Madrid_section'])
    dataN = dataN.astype(float)

    dataN.reset_index(drop=True, inplace=True)
    scaler = MinMaxScaler()
    dataN = power_transform(dataN, method='yeo-johnson')
    dataN = scaler.fit_transform(dataN)

    X = dataN[:,0:22]
    y = dataN[:,22]


    nof_list=np.arange(1,5)     
    print(nof_list)       
    high_score=0
    nof=0           
    score_list =[]
    for n in range(len(nof_list)):
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state = 0)
        fs = sr.RReliefF(n_features = nof_list[n])
        relief = Pipeline([('fs', fs), ('m', RandomForestRegressor())])
        relief.fit(X_train,y_train)
        score = relief.score(X_test,y_test)
        score_list.append(score)
        print(f'NOF: {nof_list[n]}, Score: {score}')
        if(score > high_score):
            high_score = score
            nof = nof_list[n]

    print (print(f'High Score: NOF: {nof}, Score: {high_score}'))


def main():
    print('\nSTART FEATURE SELECTION')
    path = os.getcwd()
    feature_selection(path)