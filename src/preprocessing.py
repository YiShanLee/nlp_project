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

# TODO:
# csv soll als array von array aufgebaut werden
# also [ [a, b, c], [d, e, f]] aus "a b c \n d e f\n"

def load_data(file_path):
    corpus = []
    file_name = os.path.basename(file_path)
    with open(file_path, 'r') as f:
        while(f.readline()):
            document = f.readline()
            corpus.append(document)
    return corpus, file_name

def tokenize(document):
    return nltk.word_tokenize(document)

def to_lowercase(tokens):
    return [word.lower() for word in tokens]

# source: https://stackoverflow.com/a/38734861 & https://machinelearningmastery.com/clean-text-machine-learning-python/
def remove_punctuation(tokens):
    punctuation_set = string.punctuation.replace('-', '')  # preserve words like 'computing-related'
    table = str.maketrans('', '', punctuation_set)
    stripped = [w.translate(table) for w in tokens]
    return list(filter(None, stripped))  # filter out empty strings


def remove_stopwords(tokens):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    return [word for word in tokens if not word in stop_words]


def remove_numbers(tokens):
    return [word for word in tokens if not word.isdigit()]



#
# # TODO:
# ''' STEPS:
#     - eliminate punctuation [x]
#     - convert to lowercase [x]
#     - convert numbers into words [x]
#     - expand abbreviations??? 
#     - remove special chars? [x]
#     - remove words of length == 1
#     - what else?
# '''

def remove_unwanted_chars(data):
    return [token for token in data if token.isalpha()]

def remove_short_words(data):
    return [token for token in data if len(token) > 1]

def normalize(tokens):
    normalized_tokens = to_lowercase(tokens)
    normalized_tokens = remove_stopwords(normalized_tokens)
    normalized_tokens = remove_unwanted_chars(normalized_tokens)
    normalized_tokens = remove_short_words(normalized_tokens)
    return normalized_tokens
  

# source: Johannes
def lemmatize(data):
    lemmatizer = nltk.WordNetLemmatizer()
    return [lemmatizer.lemmatize(t,get_wordnet_pos(t)) for t in data]

# source: Johannes
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": nltk.corpus.wordnet.ADJ,
                "N": nltk.corpus.wordnet.NOUN,
                "V": nltk.corpus.wordnet.VERB,
                "R": nltk.corpus.wordnet.ADV}

    return tag_dict.get(tag, nltk.corpus.wordnet.NOUN)



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path of file to preprocess")
    parser.add_argument("--lemmatization", type=bool, help="lemmatize tokens (default=True)", default=True)
    parser.add_argument("--stemming", type=bool, help="stem tokens (default=False)", default=False)

    return parser.parse_args()

def save(data, file_name):
    print("save to file...")
       
    subpath = "../../processed/"
    path = os.path.join(os.getcwd(), subpath)

    file_path = path + file_name.replace(".csv", "_cleaned.csv")

    if not os.path.isdir(path):
        os.makedirs(path)
  
    with open(file_path, 'w') as f:
        for item in data:
            f.write(str(item).replace('[', '').replace(']', '') + '\n')
        
        print("Data written to", file_path)



def main():
  
    # check python version first
    if sys.version_info < (3, 3):
        sys.exit("Please run with python3")

    args = parse_arguments()
  
    if not os.path.isfile(args.file):
        print("error: file does not exist")
        sys.exit()

    raw_data, file_name = load_data(args.file)

    tokenized = []
    for document in raw_data:
        tokens = tokenize(document)
        tokens = normalize(tokens)
        tokenized.append(tokens)

    print(tokenized)

    #save(tokenized, file_name)


if __name__ == "__main__":
    print("Begin preprocessing...")
    main()
    print("Preprocessing finished")
    

