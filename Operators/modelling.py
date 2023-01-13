import os
import utils 
import numpy as np
import pandas as pd

from feature_generation import splitting
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

model1 = {'n_estimators': [445], 'min_samples_split': [2], 'min_samples_leaf': [1], 'max_features': [None], 'max_depth': [450], 'bootstrap': [True]}
model2 = {'n_estimators': [693], 'min_samples_split': [2], 'min_samples_leaf': [1], 'max_features': [None], 'max_depth': [340], 'bootstrap': [True]}

def training(X_train,y_train,params = False):
    """
    Trains the Random Forest if `gridSearch` is True, also finds the best
    hyperparameters in any dataset.
    """
    if params:
        parameters = params
    else:
        n_est = [int(x) for x in np.linspace(start = 50, stop = 1500, num = 10)]
        max_d = [int(x) for x in np.linspace(10, 1000, num = 10)]
        max_d.append(None)
        parameters = {'n_estimators': n_est, 'max_features': [None,'sqrt'], 'bootstrap': [True], 'max_depth': max_d, 'min_samples_split': [2,5], 'min_samples_leaf': [1, 2, 4]}  

    model = RandomForestRegressor()
    forest = RandomizedSearchCV(model, parameters, n_iter = 100, cv = 5, verbose=1, random_state=1, n_jobs = -1)
    forest.fit(X_train, y_train)
    return forest

def validation(X_train, X_test, y_train, y_test,forest):
    """
    Outputs all the validation metrics for regressor models
    """
    best_model = forest.best_estimator_
    test_acc = best_model.score(X=X_test, y=y_test)
    train_acc = best_model.score(X=X_train, y=y_train)
    print(f'    - R^2: {{ train: {train_acc:.3f}, CV: {forest.best_score_:.3f}, test: {test_acc:.3f}}}')
    print(f'    - Train metrics')
    utils.regression_results(y_train, forest.predict(X_train))
    print(f'    - Test metrics')
    utils.regression_results(y_test, forest.predict(X_test))

def visualization(X_test, y_test, forest,folder):
    """
    Visualizer of Random Forests
    """
    best_model = forest.best_estimator_

    # Feature importance based on mean decrease in impurity
    importances = best_model.feature_importances_
    std = np.std([tree.feature_importances_ for tree in best_model.estimators_], axis=0)
    forest_importances = pd.Series(importances, index=X_test.columns)
    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
    plt.savefig(f'./{folder}/RF_decrease_in_impurity')
    plt.clf()
    print(f'    - First RF visualization stored in {folder} folder')

    # Feature importance based on feature permutaation
    result = permutation_importance(
        best_model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
    )
    forest_importances = pd.Series(result.importances_mean, index=X_test.columns)
    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importances using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.savefig(f'./{folder}/RF_feature_permutation')
    plt.clf()
    print(f'    - Second RF visualization stored in {folder} folder')

def main1():
    print('\nSTART MODELLING')
    path = os.getcwd()
    X_train, X_test, y_train, y_test = utils.load_data(f'{path}/model1')
    
    print(' - TRAINING Random Forest..')
    print('   Do you want to tunne hyperparameters? (48min) y/n')
    gridSearch = input('')
    gridSearch = True if gridSearch.strip() == 'y' else False
    forest = training(X_train,y_train) if gridSearch else training(X_train,y_train,model1) 
    print('Best hyperparameters:',  forest.best_params_)
    
    print(' - VALIDATING Random Forest')
    validation(X_train, X_test, y_train, y_test, forest)
    
    print(' - VISUALIZING Random Forest')
    visualization(X_test,y_test,forest,'model1')

def main2(df):
    print('\nSTART FINAL MODEL w/ features of feature selection')
   
    df = df[['Madrid_section','single_women_aged_16_to_64','single_men_aged_65_or_over','two_adults_over_35_and_one_adult_from_16_to_34', 'two_adults_and_three_or_more_minors','single_men_aged_16_to_64','five_adults_and_0_or_more_minors','four_adults_and_0_or_more_minors','Extrangeros']]
    X_train, X_test, y_train, y_test = splitting(df,'model2')

    print(' - TRAINING Random Forest..')
    print('   Do you want to tunne hyperparameters? (48min) y/n')
    gridSearch = input('')
    gridSearch = True if gridSearch.strip() == 'y' else False
    forest = training(X_train,y_train) if gridSearch else training(X_train,y_train,model2) 
    print('Best hyperparameters:',  forest.best_params_)
    
    print(' - VALIDATING Random Forest')
    validation(X_train, X_test, y_train, y_test, forest)
    
    print(' - VISUALIZING Random Forest')
    visualization(X_test,y_test,forest,'model2')
