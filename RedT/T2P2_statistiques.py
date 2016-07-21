# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 23:34:14 2015

@author: roms
"""

# imports et fonctions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (8, 4)})
sns.set_style("darkgrid")

def stats(df):
    print('----------------------------------------')    
    print('dataset size: ' + str(len(df)))    
    for col in df.columns.tolist():
        try:
                s = df[col]
                s2 = s.dropna()
                print('----------------------------------------')
                print('COLUMN: ' + col)
                print('MIN: ' + str(min(s2)))
                if type(s.values[1]) in [np.int64, np.float64]: print('AVG: ' + str(s2.mean()))
                print('MAX: ' + str(max(s2)))
                print('NaN: ' + str(len(s)-len(s2)))
                print('uniques: ' + str(len(s.unique())))
                # if numerical, plots disstribution, if not, plots barchart
                if type(s.values[1]) in [np.int64, np.float64]:
                    plt.hist(df[col].dropna().values, 100, histtype="stepfilled", alpha=.7);
                    plt.title(col)
                    plt.show()
                elif(len(df[col].value_counts()) < 50):
                    df[col].value_counts().plot(kind = 'barh')
                    plt.show()
                else:
                    plt.hist(df[col].value_counts().dropna().values, 100, histtype="stepfilled", alpha=.7);
                    plt.title(col)
                    plt.show()
        except Exception as inst:
            print('/!\ error on column: ' + col)
            print(type(inst))     # the exception instance
            print(inst.args)      # arguments stored in .args
            print(inst)
            pass
        input() # pauses the loop

def incoherences(df, cle_tri, variable_etude, index = 'NumVeh'):
    df = df[cle_tri + [variable_etude]].sort(cle_tri)
    df['previous'] = df[index].shift(1)
    df['diff_negative'] = df[cle_tri + [variable_etude]].sort(cle_tri)[variable_etude].diff() < 0
    errors = df[(df[index] == df['previous']) & (df['diff_negative'])][index].unique().tolist()
    return errors

def heatmap(df):
    plt.pcolor(df)
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
    plt.show()

def main(tramesRef):
    # analyse exploratoire
    stats(tramesRef)


if __name__ == '__main__':
    import sys
    sys.path.append('/home/roms/Desktop/Data Fil Rouge/DataMaster.zip (2)_FILES')
    import trames2_chargement
    tramesRef = trames2_chargement.main()
    
    # merge toutes les données
    '''
    # pré analyse
    len(trames)
    len(pannes)
    len(pannesComm)
    len(referencesVin)
    len(referencesPdv)
    
    len(trames['NumVeh'].unique())
    len(pannes['﻿NumVeh'].unique())
    len(pannesComm['﻿NumVeh'].unique())
    len(referencesVin['NumVeh'].unique())
    len(referencesVin['Code point de vente'].unique())
    len(referencesPdv.index.unique())
    '''
    
    # pour les dates
    x = tramesRef['DAT_COP'].apply(lambda line : line[:10]).value_counts().sort_index
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1,)
    n, bins, patches = ax.hist(x, bins=100, histtype='bar')
    ax.set_xticklabels(x, rotation='vertical')
    #ax.set_xticklabels([n], rotation='vertical')
    
    # etudes des trames artificielles
    arti = tramesRef[tramesRef['ETAT']=='Trame artificielle']
    stats(arti)
    vehicules = arti['NumVeh'].unique().tolist()
    
    vehiculesTest = tramesRef['NumVeh'].apply(lambda x : x in vehicules)
    len(arti) # 1633 trames
    len(tramesRef[vehiculesTest]['NumVeh']) # 62958 trames
    # un exemple:
    tramesRef[tramesRef['NumVeh'] == 'V126450'][['TYP_REL', 'DAT_COP', 'DAT_VEH', 'KM_TOT', 'ETAT']].sort('DAT_COP')