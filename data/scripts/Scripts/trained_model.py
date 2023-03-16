import argparse

import gensim
# from gensim.models import FastText
import os
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)

FASTTEXT = "fastText"


class FastText(object):
    def __init__(self, model_file):
        try:
            self.model = gensim.models.FastText.load(model_file)
        except Exception as e:
            LOGGER.warning(e)

    def find_similar_to(self, positive_example=None, negative_example=None):
        similarities = self.model.wv.most_similar(positive=positive_example, negative=negative_example)
        most_similar = similarities[0]
        print("word most similar to %s is %s" % (positive_example, most_similar))

    def is_in_model(self, word):
        return word in self.model


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_file", help="File path to model (required)")
    parser.add_argument("model_type", help="Type of model, e.g. fastText (required)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    print("Is file? %s" % (os.path.isfile(args.model_file)))

    if args.model_type == FASTTEXT:
        ft_model = FastText(args.model_file)
        ft_model.find_similar_to(positive_example=["economy"], negative_example=["software"])
        ft_model.find_similar_to(positive_example=["economy"])
        print("Is '%s' contained in model? %s" % ("economy", ft_model.is_in_model("economy")))

