import argparse
import logging
import sys
import datetime
from abc import ABC, abstractmethod
from nltk.corpus import wordnet, brown
from collections import Counter
from nltk.probability import FreqDist

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)
ERROR_CODE = -1

# todo moeglichkeit auch andere nltk corpora zu retrieven, zb brown corpus

''' Abstract base class. '''


def test():
    print("********test********")


class Corpus(ABC):
    def __init__(self, corpus):
        self.corpus = corpus

    ''' Return a set of all words contained in corpus'''

    def get_words(self):
        return set(self.corpus.words())

    def bag_of_words(self):
        pass

    @abstractmethod
    def word_freq(self):
        pass

    @abstractmethod
    def most_common(self):
        pass

    @abstractmethod
    def least_common(self):
        pass


class BrownCorpus(Corpus):
    def __init__(self):
        self.corpus = brown
        self.name = "Brown"
        self.fd = self.word_freq()
        super(Corpus, self).__init__()

    def word_freq(self):
        print("inside")
        freq_dist = FreqDist()

        for sentence in self.corpus.sents():
            for word in sentence:
                word = word.lower()
                freq_dist[word] += 1

        return freq_dist

    def most_common(self, n):
        return self.fd.most_common(n)

    def least_common(self, n):
        return self.fd.most_common()[:-n - 1:-1]


class WordnetCorpus(Corpus):
    def __init__(self, lang):
        self.corpus = wordnet
        self.name = 'WordNet'
        super(Corpus, self).__init__()

    def get_synsets(self, word):
        return self.corpus.synsets(word)

    def get_synonyms_from_synsets(self, synsets, verbose=False):
        if verbose:
            TAG = self.get_synonyms_from_synsets.__name__
            MSG = "%s: synsets = %s, length = %d" % (TAG, synsets, len(synsets))
            print(MSG)

        synonyms = []
        for synset in synsets:
            for lemma in synset.lemmas():
                synonyms.append(lemma.name())
        return synonyms

    def get_synonyms(self, word, verbose=False):
        tag = self.get_synonyms.__name__
        if verbose:
            msg = "Retrieve synonyms for '{0}'...".format(word)
            pretty_print(tag, msg)

        synsets = self.get_synsets(word)
        synonyms = self.get_synonyms_from_synsets(synsets)

        if verbose:
            msg = "Retrieved synonyms for '{0}' are: {1}".format(word, synonyms)
            pretty_print(tag, msg)

        return synonyms

    def get_antonyms_from_synsets(self, synsets, verbose=False):
        if verbose:
            TAG = self.get_antonyms_from_synsets.__name__
            MSG = "%s: synsets = %s, length = %d" % (TAG, synsets, len(synsets))
            print(MSG)

        antonyms = []
        for synset in synsets:
            for lemma in synset.lemmas():
                if lemma.antonyms():
                    for antonym in lemma.antonyms():
                        antonyms.append(antonym.name())
        return antonyms

    def get_antonyms(self, word, verbose=False):
        tag = self.get_antonyms.__name__
        if verbose:
            msg = "Retrieve antonyms for '{0}'...".format(word)
            pretty_print(tag, msg)

        synsets = self.get_synsets(word)
        antonyms = self.get_antonyms_from_synsets(synsets)

        if verbose:
            msg = "Retrieved antonyms for '{0}' are: {1}".format(word, antonyms)
            pretty_print(tag, msg)

        return antonyms

    """
    
    Returns the set of unique values contained in a list.
    
        - lst: list of str
    
    """

    def get_lemmas(self, word):
        lemmas = []
        for word in self.get_synsets(word):
            for lemma in word.lemmas():
                lemmas.append(lemma.name())
        return lemmas

    ''' Not possible as such withc Wordnet corpus?'''
    def word_freq(self):
        pass

    def unique_values(self, lst):
        return set(lst)

    def most_common(self, n):
        pass

    def least_common(self, n):
        pass

    def bag_of_lemmas(self, word):
        lemmas = self.get_lemmas(word)
        bol = Counter(lemmas)
        print(bol)


def pretty_print(tag, msg):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("%s %s: %s" % (time, tag, msg))


def parse_arguments():
    languages = sorted(wordnet.langs())
    languages = str(languages)[1:-1]
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", help="Corpus you want to work with. Available corpora are: TODO")
    parser.add_argument("-lang", default="eng",
                        help="ISO-639 language code. Default is 'eng'. Available options: %s" % languages)
    parser.add_argument("-query", default=None, help="Term to query Wordnet corpus")
    parser.add_argument("-most_common", default=200, help="Number of most frequent words in Wordnet corpus. Default "
                                                          "is '200'.")
    parser.add_argument("-least_common", default=200, help="Number of least frequent words in Wordnet corpus. Default "
                                                           "is '200'.")
    return parser.parse_args()


def get_arguments(args):
    return args.corpus, args.lang, args.query, args.most_common, args.least_common


def process_brown_corpus(corpus):
    print("10 most common", corpus.most_common(10))
    print("10 least common", corpus.least_common(10))
    print(len(corpus.get_words()))
    print(type(corpus.get_words()))


def main():
    args = parse_arguments()
    corpus_name, lang, query, most_common, least_common = get_arguments(args)

    LOGGER.info("Chosen language is %s" % lang)
    LOGGER.info("Given params: corpus={4}, "
                "lang={0}, "
                "query={1}, "
                "most_common={2}, "
                "least_common={3}".
                format(lang, query, most_common, least_common, corpus_name))

    if corpus_name == 'brown':

        process_brown_corpus(corpus=BrownCorpus())

    elif corpus_name == 'wordnet':
        corpus = WordnetCorpus(args.lang)
    else:
        pass

    # TODO: change lines of code depending on what corpus can do????
    if query is not None:
        try:
            print("Querying for -query={0}".format(query))
            my_syns = corpus.get_synsets(query)
            print("synonyms for %s: %s" % (query, corpus.unique_values(corpus.get_synonyms(query))))
            print("antonyms for %s: %s" % (query, corpus.unique_values(corpus.get_antonyms(query))))
            lemmas = corpus.get_lemmas(query)
            print(lemmas)
            corpus.bag_of_lemmas(query)

            # Corpus.bag_of_words()
        except Exception as e:
            LOGGER.warning(e)
    else:
        if corpus_name == 'wordnet':
            LOGGER.info("For querying Wordnet corpus, set -query to some value, e.g. -query=test")

            print(corpus.get_words())

            sys.exit(ERROR_CODE)

        # todo shit den man so mit dem brown corpus machen kann


if __name__ == "__main__":
    main()
