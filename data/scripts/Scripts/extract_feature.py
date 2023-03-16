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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

def tokenize_corpus(raw_corpus):
    print("inside tokenize_corpus")
    tokenized_corpus = []
    for document in raw_corpus:
        tokens = tokenize(document)
        tokens = remove_unwanted_chars(tokens)
        
        if len(tokens) > 0:
            tokenized_corpus.append(tokens)
    
    return tokenize_corpus
    
def remove_unwanted_chars(data):
    tokenized_corpus = []
    for token in data:
        token = token.strip("\'")
        tokenized_corpus.append(token)
        #print(token)
    return [token for token in tokenized_corpus if token.isalpha()]

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path of file to preprocess")
    parser.add_argument("model", help="feature/model to extract, e.g. model = 'bow' for bag of words")
    parser.add_argument("--tokenized", help="whether corpus contains single tokens or sentences (default: tokens=True)", default=True) #assume by default corpus already tokenized
    parser.add_argument("--filename", help="file name under which plot(s) should be saved", default="fig")

    return parser.parse_args()

def save(data, file_name):
    print("save to file...")
       
    subpath = "../../processed/"
    path = os.path.join(os.getcwd(), subpath)

    file_path = path + file_name.replace(".csv", "_cleaned_again.csv")

    if not os.path.isdir(path):
        os.makedirs(path)
  
    with open(file_path, 'w') as f:
        for item in data:
            f.write(str(item).replace('[', '').replace(']', '') + '\n')
        
        print("Data written to", file_path)

def join_tokens(corpus, output='array'):
    new_corpus = None
    if output == 'array':
        new_corpus = []
        for document in corpus:
            d = " ".join(document)
            new_corpus.append(d)
    elif output == 'string':
        new_corpus = ''
        for document in corpus:
            d = " ".join(document)
            new_corpus += d
    else:
        new_corpus = corpus # do nothing basically
    return new_corpus

def bag_of_words(corpus, tokens, top_n=None):

    if tokens:
        # join tokens into sentence again as required by CountVectorizer
        corpus = join_tokens(corpus)
    vectorizer = CountVectorizer(max_features=top_n)
    X = vectorizer.fit_transform(corpus)#
    feature_names = vectorizer.get_feature_names()
    counts = X.toarray().ravel()
    # normalize                                                                                                                                             
    counts = counts / float(counts.max())

    # print(X.toarray())
    # print(feature_names)
    #print(corpus[-1])

    return X, feature_names, counts

def flatten_array(data):
    arr = []
    for row in data:
        for col in row:
            arr.append(col)
    return arr

def count_frequency(corpus):
    tokenized_corpus = flatten_array(corpus)

    return Counter(tokenized_corpus)

def visualize_bow(X, n):
    X = X.todense()
    
    # Dimension reduction with PCA
    pca = PCA(n_components=2).fit(X)
    
    data2D = pca.transform(X)
    plt.scatter(data2D[:,0], data2D[:,1])
    plt.show() 

def word_cloud(bow, file_name): #tokenized, file_name):
    file_extension = ".png"
    if file_name[-4:] != file_extension:
        file_name += file_extension
    
    file_path = "/home/carina/Documents/Uni/WS-19-20/NLP-Projekt/Git/nlp-projekt/data/figures/word_clouds/" + file_name

    print("file name", file_name)
    # if tokenized:
    #     corpus = join_tokens(corpus, output='string')

    stopwords = set(nltk.corpus.stopwords.words('english'))
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate_from_frequencies(bow)
  
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.savefig(file_path)
    print("Saved file to ", file_path)
    plt.show()

def bigrams(data):
    return ngrams(data, 2)

def trigrams(data):
    return ngrams(data, 3)
    
def main():
  
    # check python version first
    if sys.version_info < (3, 3):
        sys.exit("Please run with python3")

    args = parse_arguments()
  
    if not os.path.isfile(args.file):
        print("error: file does not exist")
        sys.exit()

    raw_data, file_name = load_data(args.file)


    tokenized_corpus = []
    for document in raw_data:
        tokens = tokenize(document)
        tokens = remove_unwanted_chars(tokens)
        
        if len(tokens) > 0:
            tokenized_corpus.append(tokens)


    if args.model == "bow":
        num_of_words = 200
        bow_vectorized, feature_names, counts = bag_of_words(tokenized_corpus, args.tokenized)
        bow_dict = count_frequency(tokenized_corpus) # simple frequency bow dictionary
        #print(bow_vectorized)
        #print('one' in feature_names)
        #print("counts", counts)
        #print(bow_dict.most_common(4))
        #visualize_bow(bow, num_of_words)
        word_cloud(bow_dict, args.filename)

        #print(bow_dict)

    print("TOKENIZED ****************************************************")
    print(tokenized_corpus[0][:10])
    print(len(tokenized_corpus))


if __name__ == "__main__":
    print("Begin preprocessing...")
    main()
    
    print("Preprocessing finished")
    

