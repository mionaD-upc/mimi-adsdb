import os, sys
import utils 
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import power_transform
from sklearn.pipeline import Pipeline
import sklearn_relief as sr
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

def feature_selection(path):
    data = utils.DBtable_to_df('../integration.duckdb', 'integratedTable')
    dataN = data.drop(columns=['Year','Madrid_section'])
    dataN = dataN.astype(float)

    l = len(dataN.columns)
    cols  =  dataN.columns.to_list()

    dataN.reset_index(drop=True, inplace=True)

    scaler = MinMaxScaler()

    dataN = power_transform(dataN, method='yeo-johnson')
    dataN = scaler.fit_transform(dataN)

    X = dataN[:,0:l-1]
    y = dataN[:,l-1]

    np.random.seed(144)
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state = 0)
    r = sr.RReliefF(n_features = 5)
    r.fit_transform(X_train,y_train)
    values = r.w_
    res = dict(zip(cols, values))

    #print(sorted(res.items(), key=lambda x:x[1],reverse=True))
    print("Top five important features based on RReliefF Filter Method")
    print(dict(sorted(res.items(), key=lambda x:x[1],reverse=True)[0:5]).keys())

    np.random.seed(144)
    nof_list=np.arange(1,11)     
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
        if(score > high_score):
            high_score = score
            nof = nof_list[n]
        print('Highest Score for Number of Features used in RReliefF Wrapper Method:')
        print(high_score)

def main():
    print('\nSTART FEATURE SELECTION')
    path = os.getcwd()
    feature_selection(path)