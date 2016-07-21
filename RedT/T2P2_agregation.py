# -*- coding: utf-8 -*-

# imports et fonctions
import pandas as pd

def agregationTrames(trames):
    # crée les étiquettes des variables
    variables_alt = trames.columns[-24:-2].tolist()
    variables_num = ['KM_TOT', 'DIST_BTA', 'NIV_CAR', 'TEMP_EAU_MOT', 'TEMP_HUI_MOT'\
                     ,'CONS_MOY', 'ALTITUDE']
    variables_str = ['Libellé Marque', 'Code Famille Indicateur', 'Code Energie',
                     'Code Type Moteur', 'Code du Segment', 'Code Plateforme',
                     'Code Responsabilité', 'Annee Entree Garantie', 'Libelle Pays']
    index = 'NumVeh'
    
    # agrège les variables numériques
    max_ = trames[[index] + variables_num].groupby(index).max()
    max_.columns = [l + '_max' for l in max_.columns]
    min_ = trames[[index] + variables_num].groupby(index).min()
    min_.columns = [l + '_min' for l in min_.columns]
    avg_ = trames[[index] + variables_num].groupby(index).mean()
    avg_.columns = [l + '_avg' for l in avg_.columns]
    std_ = trames[[index] + variables_num].groupby(index).std()
    std_.columns = [l + '_std' for l in std_.columns]
    alertes = trames[[index] + variables_alt].groupby(index).max()
    trames_grp = pd.concat((max_, min_, avg_, std_, alertes), join='inner', axis=1)
    
    # agrège les variables catégorielles
    trames_str_grp = trames[[index] + variables_str].groupby(index).first()
    for column in trames_str_grp.columns:
        labels =  trames_str_grp[column].value_counts().index.tolist()
        trames_grp = pd.concat((trames_grp, 
                                pd.get_dummies(trames_str_grp[column])[labels[:-1]]\
                                ), join='inner', axis=1)
    del trames_str_grp
    
    # retraite certaines valeurs aberrantes (au-dessus de 1000 par exemple)
    trames_grp['CONS_MOY_max'][trames_grp['CONS_MOY_max'] > 100] = 100
    trames_grp['CONS_MOY_min'][trames_grp['CONS_MOY_min'] > 100] = 100
    trames_grp['CONS_MOY_avg'][trames_grp['CONS_MOY_avg'] > 100] = 100
    trames_grp['CONS_MOY_std'][trames_grp['CONS_MOY_std'] > 100] = 100
    return trames_grp


def agregationPannes(pannes):
    return pannes['﻿NumVeh'].value_counts().index


def main(data, nom):
    if(nom == 'trames'):
        return agregationTrames(data)
    elif(nom == 'pannes'):
        return agregationPannes(data)
    else:
        return print('Input must be in [\'trames\', \'pannes\']')
