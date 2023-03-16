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

# TODO:
# csv soll als array von array aufgebaut werden
# also [ [a, b, c], [d, e, f]] aus "a b c \n d e f\n"

# TODO: stopwords == 1 entfernen
def load_data(file_path):
    print("inside load_data\n")
    lst = []
    fname = os.path.basename(file_path)
    with open(file_path, 'r') as f:
        while(f.readline()):
            line = f.readline()
            #print("line", line)
            #print("\n")
            lst.append(line)
    return lst, fname


    # f = open(file_path, 'rt')
    # file_content = f.readline()
    # f.close()
    #return file_content, fname


def tokenize(data):
    tokenized = []
    for line in data:
        tokens = nltk.word_tokenize(line)
        tokenized.append(tokens)
    return tokenized


def to_lowercase(data):
    tokenized = []
    for line in data:
        tokens = [word.lower() for word in line]
        tokenized.append(tokens)
        print("lowercase tokens", tokens)
    return tokenized

# source: https://stackoverflow.com/a/38734861 & https://machinelearningmastery.com/clean-text-machine-learning-python/
def remove_punctuation(tokens):
    punctuation_set = string.punctuation.replace(
        '-', '')  # preserve words like 'computing-related'
    table = str.maketrans('', '', punctuation_set)
    stripped = [w.translate(table) for w in tokens]
    return list(filter(None, stripped))  # filter out empty strings


def remove_stopwords(data):
    tokenized = []
    stop_words = set(nltk.corpus.stopwords.words('english'))

    for line in data:
        tokens = [word for word in line if not word in stop_words]
        tokenized.append(tokens)
    return tokenized


def remove_numbers(data):
    tokenized = []
    for line in data:
        tokens = [word for word in line if not word.isdigit()]
        tokenized.append(tokens)
    return tokenized

# TODO:
''' STEPS:
    - eliminate punctuation [x]
    - convert to lowercase [x]
    - convert numbers into words [x]
    - expand abbreviations??? 
    - remove special chars? [x]
    - remove words of length == 1
    - what else?
'''

def remove_unwanted_chars(data):
    tokenized = []
    for line in data:
        tokens = [token for token in line if token.isalpha()]
        tokenized.append(tokens)
    return tokenized

def normalize(tokens):
    
    normalized_tokens = to_lowercase(tokens)
    normalized_tokens = remove_unwanted_chars(normalized_tokens)
    #normalized_tokens = remove_punctuation(normalized_tokens)
    normalized_tokens = remove_stopwords(normalized_tokens)
    #normalized_tokens = remove_numbers(normalized_tokens)
    return normalized_tokens

# source: Johannes
def lemmatize(data):

    lemmatizer = nltk.WordNetLemmatizer()

    tokenized = []
    for line in data:
        tokens = [lemmatizer.lemmatize(t,get_wordnet_pos(t)) for t in line]
        tokenized.append(tokens)
    return tokenized

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

def save(data, fname):
    print("save to file...")
       
    subpath = "../../processed/"
    path = os.path.join(os.getcwd(), subpath)

    file_path = path + fname

    if not os.path.isdir(path):
        os.makedirs(path)
  
    with open(file_path, 'w') as f:
        print("yay")
        #writer = csv.writer(f)
        for item in data:
            f.write(str(item).replace('[', '').replace(']', '') + '\n')
            #wr.writerow(data)
        
        print("Data written to", file_path)

def main():
  
    # check python version first
    if sys.version_info < (3, 3):
        sys.exit("*** Please call script with python3 ***")

    args = parse_arguments()
  
    if not os.path.isfile(args.file):
        print("error: file does not exist")
        sys.exit()
    else:
        print("file exists")

    raw_data, fname = load_data(args.file)
    for item in raw_data:
        print(item)

    #parsed_data = parse_data(raw_data)
    
    #print(type(raw_data))
    #print(s, raw_data.count(s))

    tokens = tokenize(raw_data)
    
    #ss = "n't"
    #print(ss + " (tokens)", tokens.count(ss))
    
    ##### debug shizzle #####
    #print("before normalization:\n")
    #print(tokens[:100])

    words = normalize(tokens)
    #print("after normalization:\n")
    #print(ss + " (words)", words.count(ss))

    #print(words[:100])

    if args.lemmatization:
        words = lemmatize(words)
        print("lemmatized:\n")
        print(words[:100])

    if args.stemming:
        print("TODO: stemming")

    save(words, fname)


if __name__ == "__main__":
    print("Begin preprocessing...")
    main()
    print("Preprocessing finished")
    

