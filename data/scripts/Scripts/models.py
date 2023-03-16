import logging
import tempfile
import os
from pprint import pprint as sysout
from gensim.models.fasttext import FastText

from gensim.test.utils import datapath
from gensim.models.word2vec import LineSentence

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def fast_text(corpus_file, vocab_size):
    LOGGER.info("Build vocabulary...")


    ft_model = FastText(size=vocab_size)
    ft_model.build_vocab(corpus_file=corpus_file)
    ft_model.train(corpus_file=corpus_file, epochs=ft_model.epochs, total_examples=ft_model.corpus_count,
                   total_words=ft_model.corpus_total_words)

    sysout(ft_model)
    return ft_model


def word_vector_lookup(model, word_vector):  # check ob das ueberhaupt bei allen geht oder nzr bei FT z.B.
    sysout(model[word_vector])


vocab_size = 100
corpus_file = datapath('lee_background.cor')
sentences = LineSentence(corpus_file)
sentences2 = [["cat", "say", "meow"], ["dog", "say", "woof"]]
print("sentence2 length: %d" % len(sentences2))
ft_model = fast_text(sentences2, vocab_size=11)
#

print("\nsimiliarity to raven:")
word_vector_lookup(ft_model, "raven")

# TODO: numpy reshape 2d array in 1d mit corpus und dann mal testen
# ft_model = FastText(min_count=1)
# ft_model.build_vocab(sentences=sentences2)
# ft_model.train(sentences=sentences, total_examples=ft_model.corpus_total_words, epochs=1)