# -*- coding: utf-8 -*-

import pandas as pd

def main(variable):
    # chemins des fichiers de trames
    tramesFile = '/home/roms/Documents/dataProjetFilRouge/DataMaster.zip (2)_FILES/TramesSITELanonymes.txt'
    tramesFile = '/home/roms/Desktop/Data Fil Rouge/Trames 2014/TramesSITELanonymes_2014.txt'
    pannesFile = '/home/roms/Documents/dataProjetFilRouge/DataMaster.zip (2)_FILES/DefaillanceVehActifsAnonyme.txt'
    pannesCommFile = '/home/roms/Documents/dataProjetFilRouge/DataMaster.zip (2)_FILES/DefaillanceVehActifsCommentairesAnonyme.txt'
    referencesVinFile = '/home/roms/Documents/dataProjetFilRouge/DataMaster.zip (2)_FILES/DefVehBTAanonyme - Copie.txt'
    referencesPdvFile = '/home/roms/Documents/dataProjetFilRouge/DataMaster.zip (2)_FILES/ReferentielPDV.txt'
    referencesPdvAltitudeFile = '/home/roms/Documents/dataProjetFilRouge/DataMaster.zip (2)_FILES/REF_PdV_Altitude.txt'
    
    # chargement en DF
    trames = pd.DataFrame.from_csv(tramesFile, sep = '\t', index_col = False)
    pannes = pd.DataFrame.from_csv(pannesFile, sep = '\t', index_col = False)
    pannesComm = pd.DataFrame.from_csv(pannesCommFile, sep = '\t', index_col = False)
    referencesVin = pd.DataFrame.from_csv(referencesVinFile, sep = '\t', index_col = False)
    referencesPdv = pd.DataFrame.from_csv(referencesPdvFile, sep = '\t')
    referencesPdvAltitude = pd.DataFrame.from_csv(referencesPdvAltitudeFile, sep = '\t')

    # merge toutes les données
    if(variable == 'trames'):
        references = pd.merge(referencesVin, referencesPdvAltitude, left_on = 'Code point de vente', right_index = True, how = 'inner').drop_duplicates()
        tramesRef = pd.merge(trames, references, left_on = 'NumVeh', right_on = 'NumVeh', how = 'inner').drop_duplicates()
        return tramesRef
    elif(variable == 'pannes'):
        return pannes
    else:
        return print('Input must be in [\'trames\', \'pannes\']')

if __name__ == '__main__':
    test = main('trames')
    test = main('pannes')