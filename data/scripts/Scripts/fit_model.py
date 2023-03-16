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

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path of preprocessed file")
    #parser.add_argument("model", help="choose which model to run")
    return parser.parse_args()

def check_python_version():
    if sys.version_info < (3,3):shutdown now
        sys.exit("Please run script with 'python3'")
def check_file(file_path):
    if not os.path.isfile(file_path):
        sys.exit("Error: file %s does not exist" % file_path)

def inspect_corpus(corpus, n):
    print("\ncontent of %d-th document: %s" % (n, corpus[n]))
  
def main():
    check_python_version()

    args = parse_arguments()

    file_path = args.file
    check_file(file_path)

    print("File path: %s" % file_path)

    raw_corpus = load_processed_data(file_path)
    split_corpus = split_and_remove_whitespaces(raw_corpus)
    corpus = remove_quotes(split_corpus)
    print("\ncorpus contains %d documents" % len(raw_corpus))

    inspect_corpus(raw_corpus, 0)
    print_out(0, 0, corpus[0][0])
    document_n = len(corpus)-1
    word_n = len(corpus[document_n])-1
    print_out(document_n, word_n, corpus[document_n][word_n])

    #tokenized_corpus = tokenize_corpus(raw_corpus)
#print(len(tokenized_corpus))

    #return

if __name__ == "__main__":
    print("Begin fitting model...")
    main()
    print("Model fitted")
    


