# -*- coding: utf-8 -*-

###############################################################################
# IMPORTS
###############################################################################

# chemin vers le dossier contenant les fichiers .py
path = '/home/roms/Desktop/Data Fil Rouge/DataMaster.zip (2)_FILES/Final'
# general packages
import pandas as pd
import sys
sys.path.append(path)
import  T2P2_chargement, T2P2_retraitements, T2P2_ajout_features, \
        T2P2_agregation, T2P2_statistiques, T2P2_modeles
# graphics
import matplotlib.pyplot as plt
import seaborn as sns
# machine learning
from sklearn.preprocessing import scale
from sklearn.metrics import roc_curve, auc

###############################################################################
# TRAITEMENT DES DONNEES
###############################################################################

# chargement des donnees
trames = T2P2_chargement.main('trames') 
pannes = T2P2_chargement.main('pannes')
codes = pd.DataFrame.from_csv('/home/roms/Desktop/Data Fil Rouge/DataMaster.zip (2)_FILES/codes_alertes.csv', )

# retraite les données (STT, la date entrée garantie, des colonnes avec les variables binaires d'alertes) et filtre les pannes
trames = T2P2_retraitements.main(trames, 'trames')
pannes = T2P2_retraitements.main(pannes, 'pannes')

# ajoute les features
T2P2_ajout_features.main(trames)['CONS_MOY']

# agrège les données par véhicule
trames_grp = T2P2_agregation.main(trames, 'trames')
del trames
pannes = T2P2_agregation.main(pannes, 'pannes')

# quelques statistiques descriptives
T2P2_statistiques.main(trames_grp)

# applique des modèles de machine learning
lr, dt, rf, X_test, y_test = T2P2_modeles.main(trames_grp, pannes)

# AUC (aire sous la courbe ROC) pour les données de test
for i, model in enumerate([lr, dt, rf]):
    if i == 0:
        fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(scale(X_test))[:, 1])
    else:
        fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
    plt.clf()
    plt.plot(fpr, tpr, label='ROC curve')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.show()
    print('AUC:', auc(fpr, tpr))

# extrait les features importantes
print('REGRESSION LOGISTIQUE')
print('Features importantes (sens négatif):')
trames_grp.columns[(lr.coef_ < -0.25).ravel()]
print('Features importantes (sens positif):')
trames_grp.columns[(lr.coef_ > 0.25).ravel()]

print('ARBRES DE DECISION')
print('Features importantes:')
trames_grp.columns[dt.feature_importances_ > 0.010]

print('FORETS ALEATOIRES')
print('Features importantes:')
trames_grp.columns[rf.feature_importances_ > 0.025]
