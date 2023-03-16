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
import logging

# TODO: add "_cleaned" part to save
# csv soll als array von array aufgebaut werden
# also [ [a, b, c], [d, e, f]] aus "a b c \n d e f\n"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def load_data(file_path):
    file_name = os.path.basename(file_path)
    f = open(file_path, "r")
    lines = [line.rstrip('\n') for line in f]
    f.close()
    print("There are %d lines in the corpus %s" % (len(lines), file_name))
    return lines, file_name

# irgendwie ist das verbuggt, rausmachen
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

def keep_nouns_verb(tokens):
    return None


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
    print(data)
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
    # if os.path.isfile(file_path):
    #     LOGGER.info("File already exists.")
    #     counter = 1
    #     while True:
    #         counter += 1
    #         new_fname = file_name.split(".csv")[0] str(counter) + ".csv"
    #         new_file_path = path + file_name

    #         if os.path.isfile(new_file_path):
    #             continue
    #         else:
    #             file_name = new_fname
    #             break

    with open(file_path, 'w') as f:
        for item in data:
            f.write(str(item).replace('[', '').replace(']', '') + '\n')
        
        print("Data written to", file_path)

def is_noun_or_verb(word):
    POS_TAG = 1
    VERB = 'V'
    NOUN = 'N'
    #LOGGER.info("Is *** %s *** a noun or verb? %s" % (word, (word[POS_TAG].startswith(VERB)) or (word[POS_TAG].startswith(NOUN))))
    return (word[POS_TAG].startswith(VERB)) or (word[POS_TAG].startswith(NOUN))

def keep_nouns_verbs(document):
    pos_tagged_doc = nltk.pos_tag(document)
    #print("first word: %s, last word: %s" % (pos_tagged_doc[0][0], pos_tagged_doc[0][-1]))
    WORD_POS = 0
    nouns_verbs = []
    
    for word_tuple in pos_tagged_doc:
        #LOGGER.info("Is (%s) a noun or verb? %s" % (word_tuple[WORD_POS], is_noun_or_verb(word_tuple)))
        if is_noun_or_verb(word_tuple):
            nouns_verbs.append(word_tuple[WORD_POS])
    return nouns_verbs

def preprocess(raw_data):
    corpus = []

    for document in raw_data:
        tokens = tokenize(document)
        tokens = normalize(tokens)
        tokens = keep_nouns_verbs(tokens)
        corpus.append(tokens)

    i = 0
    j = 0

    #LOGGER.info("len(corpus[%d]=%d), corpus[%d][%d] = %s" % (i, len(corpus[i]), i, j, corpus[i][j]))
    return corpus

def print_document(corpus, num_doc, num_words):
    print("Document %d, first %d words: %s" % (num_doc, num_words, corpus[:num_words]))

def main():
  
    # check python version first
    if sys.version_info < (3, 3):
        sys.exit("Please run with python3")

    args = parse_arguments()
  
    if not os.path.isfile(args.file):
        print("error: file does not exist")
        sys.exit()

    raw_data, file_name = load_data(args.file)

    tokenized = preprocess(raw_data)
    
    print("length of tokenized[] = %d" % len(tokenized))
    #print_document(corpus=tokenized, num_doc=0, num_words=10)

    #print(tokenized[0])
    save(tokenized, file_name)


if __name__ == "__main__":
    print("Begin preprocessing...")
    main()
    print("Preprocessing finished")
