# run with python3
import os
import sys
import argparse
import numpy as np
import pandas as pd
import nltk
import csv
import re
import string
import time

from preprocess import *

def print_out(index_document, index_word, content):
    print("document #%d word #%d is: '%s'" % (index_document, index_word, content))

def load_data(file_path):
    corpus = []
    fname = os.path.basename((file_path))
    with open(file_path, 'r') as f:
        documents = f.readlines()
        for document in documents:
            #print("document: %s" % document)
            corpus.append(document)
    return corpus


def load_data2(file_path):
    file_name = os.path.basename(file_path)
    f = open(file_path, "r")
    lines = [line.rstrip('\n') for line in f]
    f.close()
    print("There are %d lines in the corpus %s" % (len(lines), file_name))
    return lines, file_name

file_path = '/home/carina/Documents/Uni/WS-19-20/NLP-Projekt/Git/nlp-projekt/data/raw/'
file_name = 'IT_Corpus.csv'
f = file_path+file_name

print("Does file exist? %s" % (os.path.isfile(f)))

raw_corpus = load_data(f)
load_data2(f)

print("corpus contains %d documents" % len(raw_corpus))

print("test", raw_corpus[-1])
print("\n\n\n")




#tokenized_corpus = tokenize_corpus(raw_corpus)
#print(len(tokenized_corpus))
