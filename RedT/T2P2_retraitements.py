# -*- coding: utf-8 -*-

# imports et fonctions
import pandas as pd

def incoherences(df, cle_tri, variable_etude, index = 'NumVeh'):
    """
    Permet de voir si il existe des incohérences dans les dates
    """
    df = df[cle_tri + [variable_etude]].sort(cle_tri)
    df['previous'] = df[index].shift(1)
    df['diff_negative'] = df[cle_tri + [variable_etude]].sort(cle_tri)[variable_etude].diff() < 0
    errors = df[(df[index] == df['previous']) & (df['diff_negative'])][index].unique().tolist()
    return errors


def calculAlertesUniques(tramesRef):
    alertesList = tramesRef['CONCAT_AL'].dropna().apply(lambda line : line.split('/')[:-1]).tolist()
    alertesUniques = pd.DataFrame([item for sublist in alertesList for item in sublist])[0].apply(lambda line : 'AL' + line).unique().tolist()
    alertesUniques.sort() # les différentes alertes présentes
    return alertesUniques


def retraitements_trames(tramesRef):
    # retraitements
    # STT = 0 ou 1
    tramesRef['STT'] = tramesRef['STT'].fillna(0)
    # retraitements des dates à 01/01/1900
    cond = tramesRef['Date Entree Garantie'] == '01/01/1900'
    tramesRef['Date Entree Garantie'][cond] = tramesRef['Date Entrée Montage'][cond]
    # retraitement de certaines températures
    tramesRef['NIV_HUI_MOT'][tramesRef['NIV_HUI_MOT'] < 0] = 0 # niveau à -3
    tramesRef['TEMP_EAU_MOT'][tramesRef['TEMP_EAU_MOT'] > 200] = float('nan') # températures = 25k, 26k degrés. Pas de panne
    tramesRef['TEMP_HUI_MOT'][tramesRef['TEMP_HUI_MOT'] > 200] = float('nan') # températures = 25k, 26k degrés. Mêmes véhicules que précedemment
    # mettre une colonne par alerte avec des [0,1] dedans
    alertesUniques = calculAlertesUniques(tramesRef) 
    for alerte in alertesUniques: # rajoute les colonnes d'alerte au df avec les valeurs
        tramesRef[alerte] = tramesRef['CONCAT_AL'].dropna().apply(lambda line : 1 if alerte[-3:] in line else 0)
        tramesRef[alerte] = tramesRef[alerte].fillna(0)
    return tramesRef


def retraitements_pannes(pannes):
    pannes = pannes[pannes['﻿NumVeh'] != 'V105173']
    # ne filtre que les pannes de moteur
    pannes = pannes[(pannes['Type Incident'] == 'P') & (pannes['Module'] == 'GMP15 Moteur')]
    return pannes


def main(data, nom):
    if(nom == 'trames'):
        return retraitements_trames(data)
    elif(nom == 'pannes'):
        return retraitements_pannes(data)
    else:
        return print('Input must be in [\'trames\', \'pannes\']')
