# -*- coding: utf-8 -*-

def main(trames):
    trames['CONS_MOY'] = (trames['CONS_TOT'] / trames['DIST_BTA']).fillna(0)
    trames['Annee Entree Garantie'] = trames['Date Entree Garantie'].apply(lambda x : x[-4:])
    return trames