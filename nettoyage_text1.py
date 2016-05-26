# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:38:56 2016

@author: b.amoussou-djangban
"""

##############################################################################
##############################################################################

    # Scipt1 netoyage text
    # Auteur : Baruch AMOUSSOU-DJANGBAN

##############################################################################
##############################################################################

#------------ Import packages
from gensim import corpora, models, similarities
import pandas as pd
import numpy as np
import unicodedata
import re
import timeit


documentList=list(new_catalogue['Description'])

#Stopwords
from nltk.corpus import stopwords
import nltk
# chargement des stopwords français
french_stopwords = set(stopwords.words('french'))
print french_stopwords

chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&','*',\
 '(', ')', ' - ', '_', '+' ,'=', '@', ':', '\\', ',',';', '~', '`', '<',\
 '>', '|', '[', ']', '{', '}', '–', '“','»', '«', '°', '’', '--'\
 '</div>','<div','class','class="tt14-prodpres-txt' ,'tt14-prodpres-res">','<b>','</b>']



from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()
stemmer.stem('voudrais')

def cleaningDocumentList(documentList):
    #remove frech stopwords
    texts = [[word for word  in document.lower().replace("'",'').split() if word not in french_stopwords] for document in documentList]
    #remove special catalogue characters
    texts = [[word for word  in text if word not in chars] for text in texts]
    # remove french accent
    texts = [[unicodedata.normalize('NFD',unicode(word,'utf-8')).encode('ascii', 'ignore') for word  in text] for text in texts]
    #remove general special characters 
    texts = [[re.sub(r'[. ?!=+ & | , " :; ⋆ $ %()<> &\[\]/_]',r'',word) for word in text] for text in texts]
    #remove small words
    texts = [[re.sub(r'\b\w{1,3}\b', '', word) for word in text] for text in texts]
    #Lemmitizer
    texts = [[stemmer.stem(word) for word in text] for text in texts]
    #remove empty string
    texts=[[x for x in text if x] for text in texts]
    return texts

texts=cleaningDocumentList(documentList)

##" Trouver les attrubuts de mots (Verbes, adjectifs, noms....)

text = nltk.word_tokenize("And now for something completely different")
nltk.pos_tag(text)

from string import punctuation
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

# Traitement des accents
# Accent traitement
s1 = unicode('comprimé','utf-8')
s2 = unicodedata.normalize('NFD', s1).encode('ascii', 'ignore')  
