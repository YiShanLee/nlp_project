# run with python3
import os
import sys
import argparse
import logging
import numpy as np
import pandas as pd
import nltk
import csv
import re
import string
import time

from gensim.test.utils import datapath
from gensim.models.fasttext import FastText

from preprocess import load_data, remove_unwanted_chars
from nltk import word_tokenize

from gensim.test.utils import datapath
from gensim.models.fasttext import FastText
from gensim.models.word2vec import LineSentence
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.test.utils import get_tmpfile

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)

SUCCESS_MSG_TRAINING = "Successfully trained {0} model"
SUCCESS_MSG_SAVING = "Successfully saved model {0}"
FAST_TEXT = "fasttext"
TFIDF = "tfidf"

SAVE_MODEL_PROMPT = "Save model to disk? y/n"
FNAME_PROMPT = "Save model as: <modelname>"
YES = "y"
NO = "n"


def save_msg(fpath):
    SAVE_MSG = "Save model to: {0}"
    print(SAVE_MSG.format(fpath))


def prompt_user(msg):
    return input(msg)


def print_out(index_document, index_word, content):
    print("document #%d word #%d is: '%s'" % (index_document, index_word, content))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path of preprocessed file (required)")
    parser.add_argument("model", help="Name of model to train (required)")
    parser.add_argument("-size", help="Size of the model (dimensionality of vectors) (optional)", default=10)
    parser.add_argument("-window", help="Window size (optional)", default=3)
    parser.add_argument("-epochs", help="Set number of epochs (optional)", default=20)
    parser.add_argument("-min_count", help="Minimum frequency of words in corpus (optional)", default=1)
    return parser.parse_args()


def check_python_version():
    if sys.version_info < (3, 3):
        LOGGER.warning("Please run script with 'python3'")
        sys.exit(-1)


def check_file(file_path):
    if not os.path.isfile(file_path):
        LOGGER.warning("Error: file %s does not exist" % file_path)
        sys.exit(-1)


def inspect_corpus(corpus, n):
    print("\ncontent of %d-th document: %s" % (n, corpus[n]))


def tokenize(corpus):
    tokenized_corpus = []
    for document in corpus:
        tokenized_doc = word_tokenize(document)
        tokenized_doc = [token.replace("'", "") for token in tokenized_doc]
        tokenized_doc = [token for token in tokenized_doc if len(token) > 1]
        print("tokenized_doc: %s" % tokenized_doc)
        tokenized_corpus.append(tokenized_doc)
    return tokenized_corpus


'''size : int, optional
            Dimensionality of the word vectors.'''


def fast_text(corpus_file, size, window, num_epochs, min_count):
    output_msg = SUCCESS_MSG_TRAINING.format("fastText")
    sentences = LineSentence(corpus_file)
    ft_model = FastText(size=size, window=window,
                        min_count=min_count)  # instantiate # TODO: mit size und window experimiernten bzw fix memory error TODO: size=4 ist viel zu klein, wir brauchen doch mehr dimensionen sonst ist das ganze sinnlos
    ft_model.build_vocab(sentences)
    ft_model.train(sentences=sentences, total_words=ft_model.corpus_total_words, epochs=num_epochs)
    LOGGER.info(output_msg)
    return ft_model


def corpus_size(corpus):
    count = 0
    for document in corpus:
        for word in document:
            count += 1
    return count


def word_vector_lookup(model, word_vector):  # check ob das ueberhaupt bei allen geht oder nzr bei FT z.B.
    print(model[word_vector])


def save_model(model, model_type):
    user_input = prompt_user(SAVE_MODEL_PROMPT)
    if user_input == YES:
        model_name = prompt_user(FNAME_PROMPT)
        model_extsn = ".model"
        script_dir = os.path.dirname(os.getcwd())
        parent_dir = os.path.dirname(script_dir)
        model_dir = "models/" + model_type + "/"
        model_path = os.path.join(parent_dir, model_dir)
        if not os.path.isdir(model_path):
            os.mkdir(model_path)

        fname = model_path + model_name + model_extsn
        save_msg(fname)
        try:
            print("is path? %s" % (os.path.isdir(model_path)))
            model.save(fname)
            print(SUCCESS_MSG_SAVING.format(FAST_TEXT))
        except Exception as e:
            LOGGER.warning(e)
    elif user_input == NO:
        LOGGER.info("Model not saved")
        sys.exit(0)
    else:
        print("Abort")
        sys.exit(-1)


def tfidf(corpus_file):
    dict = Dictionary(corpus_file)
    # tfidf_model = TfidfModel(corpus=corpus_file)
    return dict


def clean_up(corpus):
    cleaned_corpus = []
    for document in corpus:
        cleaned_document = remove_unwanted_chars(document)
        cleaned_corpus.append(cleaned_document)
    return cleaned_corpus


if __name__ == "__main__":
    print("Begin fitting model...")
    check_python_version()
    args = parse_arguments()

    check_file(args.file)

    untokenized_corpus, corpus_name = load_data(
        args.file)  # das ding ist: der preprocessed corpus muss halt auch wieder tokenized werden, lol
    corpus = tokenize(untokenized_corpus)
    corpus = clean_up(corpus)
    total_words = corpus_size(corpus)

    print("There are %d words in corpus" % total_words)

    if args.model == FAST_TEXT:
        ft_model = fast_text(corpus_file=args.file, size=args.size, window=args.window, num_epochs=args.epochs,
                             min_count=args.min_count)
        # fname = get_tmpfile("fasttext.model")
        # ft_model.save(fname)
        word_vector_lookup(ft_model, "economics")
        save_model(ft_model, FAST_TEXT)

    if args.model == TFIDF:
        tfidf_model = tfidf(corpus_file=corpus)

    print("Model fitted")
