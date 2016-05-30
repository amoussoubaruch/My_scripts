import pandas as pd
import numpy as np
from scipy.spatial import distance

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# Read files
ge_he = pd.read_excel('EXTRACT 11 05 2016.xlsx')
ge_ca = pd.read_excel(
    'Copie de RAM_BASE INSTALLEE_ (2).xlsx', sheetname='CORE')
# check files
ge_he.head()
ge_ca.head()
# ge_he.tail()
# ge_ca.tail()

ge_he['Tier 2 P&L'].value_counts()

print "EXTRACT / RAM : %s | %s" % (ge_he.shape, ge_ca.shape)

# merge on IB
ge_he[u"IB Asset\xa0: IB Asset Name"].value_counts()  # key unique
ge_ca["IB"].value_counts()

# EXTRACT / RAM : (16772, 31) | (766, 54)

IB_dup = ["M171587018",
          "M4482628",
          "M9483440",
          "X178710401",
          "X1135608",
          "M2001106",
          "M190773205",
          "M1973723",
          "M219000205",
          "M414406703",
          "M1245717",
          "M6009611"]

ge_ca[ge_ca.IB.isin(IB_dup)].sort("IB")
match1 = pd.merge(ge_he, ge_ca, how="inner",
                  left_on=u"IB Asset\xa0: IB Asset Name", right_on="IB")
match1.IB.value_counts()
match1[u"IB Asset\xa0: IB Asset Name"].value_counts()

# As stated, the match of IB & IB Asset est fausse...
# !!! Only RAM.Tier1 == Imaging
# KEY = YEAR, TIER2, TIER3, DEP | Month, Day, Fuzzy Product
# factor of tier2
ge_he[u"Tier 2 P&L"].value_counts()
ge_ca['Tier 2'].value_counts()
# DGS, MICT, Surgery, MR ==> Ok

ge_he[u"Tier 3 P&L"].value_counts()
ge_ca['Tier 3'].value_counts()
# [u'CT', u'Women?s Healthcare (WHC)', u'Interventional (INTV)',
# u'Radiography and Radiography & Fluoroscopy (RRF)',
# u'Bone Mineral Density (BMD)', u'PET'] ==> ok , no u' ', u'OTHER'

ge_he['date'] = (ge_he["Install Date"].astype('int') / 10**9) / 86400
ge_he['dep'] = ge_he[u"Code postal de l'adresse de facturation"].astype(
    'string').str.slice(0, 2)
ge_he['lastName'] = ge_he[
    "P&L accountable - Services"].str.split().str[-1].str.split(".").str[-1].str.upper()

ge_ca['lastName'] = ge_ca[
    "Account Manager (DI ou US)"].str.split().str[-1].str.split(".").str[-1].str.upper()
ge_ca['date'] = (pd.to_datetime(
    ge_ca["DATE DE DEBUT DE CONTRAT"]).astype('int') / 10**9) / 86400
ge_ca['dep'] = ge_ca["CP "].astype(
    'string').str.slice(0, 2)

ge_he_key = ge_he[["date", u"Tier 2 P&L", u"Tier 3 P&L",
                   u"dep", 'lastName']]
ge_he_key.rename(columns={"Tier 2 P&L": "tier2",
                          u"Tier 3 P&L": "tier3"}, inplace=True)
ge_ca_key = ge_ca[["date", "Tier 2", "Tier 3", "dep", 'lastName']]
ge_ca_key.rename(columns={"Tier 2": "tier2",
                          u"Tier 3": "tier3"}, inplace=True)


mat_ge_he_key = pd.get_dummies(
    ge_he_key, columns=[u"tier2", u"tier3", u"dep", u"lastName"])
mat_ge_ca_key = pd.get_dummies(
    ge_ca_key, columns=[u"tier2", u"tier3", u"dep", u"lastName"])

set(mat_ge_ca_key.columns.values).difference(set(mat_ge_he_key.columns.values))
set(mat_ge_he_key.columns.values).difference(set(mat_ge_ca_key.columns.values))

commonColumn = list(set(mat_ge_he_key.columns.values).intersection(
    set(mat_ge_ca_key.columns.values)))
mat_ge_he_key = mat_ge_he_key[commonColumn]
mat_ge_ca_key = mat_ge_ca_key[commonColumn]


# cos distance
noDate = cols = [col for col in commonColumn if col not in ['date']]
matdist_noDate = distance.cdist(mat_ge_he_key[noDate], mat_ge_ca_key[
                                noDate], metric='euclidean')
matdist_noDate.shape

mat_ge_he_key["temp"] = 0
mat_ge_ca_key["temp"] = 0
matdist_date = distance.cdist(mat_ge_he_key[["date", "temp"]], mat_ge_ca_key[
                              ["date", "temp"]], metric='euclidean')
matdist_date.shape

matdist_noDate[matdist_noDate > 0] = np.inf
matdist_date[matdist_date > 30] = np.inf
matdist_final = (matdist_noDate + matdist_date)

res = pd.DataFrame({"ca": range(0, 766),
                    "he_noDate": np.argmin(matdist_final, axis=0),
                    "he_noDate_score": np.amin(matdist_final, axis=0)})
res.loc[res["he_noDate_score"]==np.inf, "he_noDate"] = np.nan
res
sum(res.he_noDate_score < np.inf)

len(set(res.he_noDate))

# fuzzywheezy - fuzzymatch
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import string

choices = ge_he["IB Product Name"].str.strip(
).str.replace(
    '[%s]' % re.escape(string.punctuation), " ").str.upper().values
ge_ca["LIBELLE DU MATERIEL FINANCE"].str.strip().str.replace(
    '[%s]' % re.escape(string.punctuation), " ").str.upper()
process.extract("CT OPTIMA 660", choices, limit=30)
process.extractBests("OPTIMA 660", choices, limit=30)
