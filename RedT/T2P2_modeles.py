# -*- coding: utf-8 -*-

# general
import numpy as np
import pandas as pd
# machine learning
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier

def main(trames_grp, pannes):
    # préparation des données
    y = pd.Series(-1, index = trames_grp.index)
    pannesIndex = set(pannes)
    y.ix[pannesIndex] = 1
    X = trames_grp.fillna(0)

    # on divise les données en train/tste en prenant garde d'avoir une bonne répartition pannes/non-pannes
    train_size=0.70
    train_idx = set(np.random.choice(y[y == 1].index, int(train_size * len(y[y == 1])), replace=False))
    train_idx = train_idx.union(set(np.random.choice(y[y == -1].index, int(train_size * len(y[y == -1])), replace=False)))
    test_idx = set(y.index).difference(train_idx)
    X_training = X.ix[train_idx]
    X_test = X.ix[test_idx]
    y_training = y.ix[train_idx]
    y_test = y.ix[test_idx]
       
    '''
    REGRESSION LINEAIRE
    '''
        
    # pour la régression linéaire, on centre/réduit les données avec scale    
    X_cr = pd.DataFrame(scale(X), columns=X.columns, index=X.index)
    X_training_cr = X_cr.ix[train_idx]
    X_test_cr = X_cr.ix[test_idx]

    ''' sélection de modèle, à ne faire tourner qu'une seule fois
    
    result_training=[]
    result_test=[]
    Cs=[0.01, 0.1, 1, 10]
    for C in Cs:
        lr = lr = LogisticRegression(class_weight='auto', C=C)
        lr.fit(X_training, y_training)
        fpr, tpr, thresholds = roc_curve(y_training, lr.predict_proba(X_training)[:, 1])
        result_training.append(auc(fpr, tpr))
        fpr, tpr, thresholds = roc_curve(y_test, lr.predict_proba(X_test)[:, 1])
        result_test.append(auc(fpr, tpr))
    plt.plot(np.log(Cs), result_training)
    plt.plot(np.log(Cs), result_test)
    plt.legend(['training', 'test'], loc=0)
    plt.xlabel('Complexity (log scale)')
    plt.ylabel('AUC')
    '''
        
    lr = LogisticRegression(class_weight='auto')
    lr.fit(X_training_cr, y_training)
    print('REGRESSION LOGISTIQUE')
    print(np.sum(lr.predict(X_cr) == 1), ' pannes prédites')
    print(np.sum((lr.predict(X_cr) == 1)&(y == 1)), ' pannes détectées sur un total de ', np.sum(y == 1))
       
       
    '''
    DECISION TREE
    '''
    
    ''' sélection de modèle, à ne faire tourner qu'une seule fois
    result_training=[]
    result_test=[]
    max_depths=[2,3,4,5,6]
    for max_depth in max_depths:
        dt = DecisionTreeClassifier(class_weight='auto', max_depth=max_depth)
        dt.fit(X_training, y_training)
        fpr, tpr, thresholds = roc_curve(y_training, dt.predict_proba(X_training)[:, 1])
        result_training.append(auc(fpr, tpr))
        fpr, tpr, thresholds = roc_curve(y_test, dt.predict_proba(X_test)[:, 1])
        result_test.append(auc(fpr, tpr))
    plt.plot(max_depths, result_training)
    plt.plot(max_depths, result_test)
    plt.legend(['training', 'test'], loc=0)
    plt.xlabel('Complexity')
    plt.ylabel('AUC')
    '''
    
    dt = DecisionTreeClassifier(class_weight='auto', max_depth=4)
    dt.fit(X_training, y_training)
    print('ARBRES DE DECISION')
    print(np.sum(dt.predict(X) == 1), ' pannes prédites')
    print(np.sum((dt.predict(X) == 1)&(y == 1)), ' pannes détectées sur un total de ', np.sum(y == 1))
    
    export_graphviz(dt, out_file='tree_PSA.dot', max_depth=None, feature_names=X.columns)
    # puis transformer le fichier en png via $ dot -Tpng tree_PSA.dot -o tree_PSA.png 
    
    '''
    RANDOM FORESTS
    '''
    
    ''' sélection de modèle, à ne faire tourner qu'une seule fois
    result_training=[]
    result_test=[]
    max_depths=[2,5,7,10,15]
    for max_depth in max_depths:
        rf = RandomForestClassifier(class_weight='auto', max_depth=max_depth, n_estimators=50)
        rf.fit(X_training, y_training)
        fpr, tpr, thresholds = roc_curve(y_training, rf.predict_proba(X_training)[:, 1])
        result_training.append(auc(fpr, tpr))
        fpr, tpr, thresholds = roc_curve(y_test, rf.predict_proba(X_test)[:, 1])
        result_test.append(auc(fpr, tpr))
    plt.plot(max_depths, result_training)
    plt.plot(max_depths, result_test)
    plt.legend(['training', 'test'], loc=0)
    plt.xlabel('Complexity')
    plt.ylabel('AUC')
    '''
    
    rf = RandomForestClassifier(class_weight='auto', max_depth=5, n_estimators=100)
    rf.fit(X_training, y_training)
    print('FORETS ALEATOIRES')
    print(np.sum(rf.predict(X) == 1), ' pannes prédites')
    print(np.sum((rf.predict(X) == 1)&(y == 1)), ' pannes détectées sur un total de ', np.sum(y == 1))
    
    return lr, dt, rf, X_test, y_test

