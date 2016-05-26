# -*- coding: utf-8 -*-
"""
Created on Wed May 25 10:32:07 2016

@author: b.amoussou-djangban
"""

#------------------------------------------------------------------------------
# GE : croisement de fichiers 
#------------------------------------------------------------------------------

#---- Import packages 
import pandas as pd
import numpy as np


##########                  Load  Data Train                       ########## 
report=pd.read_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\report.csv", delimiter=';')

##########                  Load  Data Test                        ########## 
ram=pd.read_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\ram.csv", delimiter=';')

type(report)

# report columns names 
report.columns.values
report.shape


# Ram 
ram.shape
ram.tail(1)
ram.columns.values

# ------------------- TEST AVEC LES ANNEES

## Fichier report 2006
report['date_annee'] = report['Install Date'].str[6:]

#l Fréquence des années 
report.groupby('date_annee')['date_annee'].count()

report_2006 = report[report['date_annee'] == '2006']

# Fichier ram 2006
ram['ANNEE DU DEBUT DU CONTRAT']
ram.groupby('ANNEE DU DEBUT DU CONTRAT')['ANNEE DU DEBUT DU CONTRAT'].count()

ram_2006 = ram[ram['ANNEE DU DEBUT DU CONTRAT'] == 2006]

#------------ Not good 

# -------------- TEST AVEC VILLE (ex rennes )

# Ficheir RAM 
ram['ville_name'] = ram['VILLE DU L.OCATAIRE'].str.lower()
ram.groupby('ville_name')['ville_name'].count()
# Select rennes villes 
ram_rennes = ram[ram['ville_name'] == 'toulouse']
# Fichier report
report['ville_name']  = report['Installation City'].str.lower()
# Select rennes villes 
report_rennes = report[report['ville_name'] == 'toulouse']

# Enregistrmeent en local pour analyse 
ram_rennes.to_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\ram_rennes.csv",sep=";", index=False)

report_rennes.to_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\report_rennes.csv",sep=",", index=False)


#-------------------------- Merge avec la clé unique  'IB'

report['IB'] = report['IB Asset\xa0: IB Asset Name']

## Merge avec RAM 

merge_IB=pd.merge(report, ram,on='IB', how='inner')

merge_IB.to_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\merge_IB.csv",sep=";", index=False)

float(49./766)*100

#-------------------------- Merge avec la clé secondaire

# Cle 1  : code postal 
report['code_postal']= report['Installation Zip/Postal Code']
ram['code_postal']=  ram['CP ']
ram['code_postal'] = ram['code_postal'].astype(float)

# Clé 2 : Install date 
ram['date_annee'] = ram['ANNEE DU DEBUT DU CONTRAT']
report['date_annee']

ram['date_annee'] = ram['date_annee'].astype(int)
report['date_annee'] = report['date_annee'].astype(int)

# - Step 1 : merge outer
result = pd.merge(ram, report, how='outer', on=['code_postal', 'date_annee'])

result.to_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\result.csv",sep=";", index=False)

result['LOCATAIRE'].isnull().sum()
result['Nom du compte'].isnull().sum()
# - Step 2 : Mesure de similarité 

# Cle 3 :  LOCATAIRE & Nom du compte
# -----------------------------------------------------------------------------
# Distance de levenshtein
# Christopher P. Matthews
# christophermatthews1985@gmail.com
# Sacramento, CA, USA

def levenshtein(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]

# -----------------------------------------------------------------------------

levenshtein('SA CLINIQUE SAINT JEAN LANGUEDOC','CENTRE SCANNER ST JEAN LANGUED')
levenshtein('SCM CENTRE RADIOLOGIE FONTAINE','CH DE FONTAINEBLEAU')

# --- deuxième mesure de similarité 
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
similar('SA CLINIQUE SAINT JEAN LANGUEDOC','CENTRE SCANNER ST JEAN LANGUED')
similar('SCM CENTRE RADIOLOGIE FONTAINE','CH DE FONTAINEBLEAU')
# Drop NA 
result1 = result[np.isfinite(result['Installation Zip/Postal Code'])]

result1 = result[result['Installation Zip/Postal Code'].notnull()]


result1.to_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\result12.csv",sep=";", index=False)

# Read new dataframe 
res=pd.read_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\result13.csv", delimiter=';')

# FRormatage string (minuscule .....)
res['String1'] = res['LOCATAIRE']
res['String2'] = res['Nom du compte']

res['levenshtein'] = res.apply(lambda row: levenshtein(row['LOCATAIRE'], row['Nom du compte']), axis=1)

res['similar'] = res.apply(lambda row: similar(row['LOCATAIRE'], row['Nom du compte']), axis=1)

res.to_csv(r"C:\Users\b.amoussou-djangban\Documents\POC Group One Point\GE\Macth_final1.csv",sep=";", index=False)

# df['Value'] = df.apply(lambda row: my_test(row['a'], row['c']), axis=1)
                                                           