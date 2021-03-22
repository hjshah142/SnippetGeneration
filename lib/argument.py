from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import numpy as np
import re


class Argument:

    def __init__(self, premises=None, context=None, id=None, conclusion=None, cluster_map=None, aspects= None):
        """
        Object representation of the args.me corpus.
        Yamen Ajjour, Henning Wachsmuth, Johannes Kiesel, Martin Potthast, Matthias Hagen, and Benno Stein. Data Acquisition for Argument Search: The args.me corpus. In 42nd German Conference on Artificial Intelligence (KI 2019), September 2019. Springer.

        :param premises: list containing dictionary with key "text" containing the argument
        :param context:
        :param id:
        :param conclusion: (str) conclustion of the argument
        :param
        cluster_map: dictionary with keys being the debate ids from the arguments. Value: List of arguments
        """

        # TODO Add cluster maps
        self.aspects = aspects
        self.premises = premises
        self.context = context
        self.id = id
        self.conclusion = conclusion
        self.sentences = []
        self.score = []

        if premises != None:
            self.set_sentences(premises)
        # cluster_map= { 1: ['Argument 1','Argument 2'] }
        self.cluster_map = cluster_map
        """"
        if cluster_map is not None:
            if context["sourceId"] in cluster_map:
                cluster_map[context["sourceId"]].append(self)
            else:
                cluster_map[context["sourceId"]] = [self]
        """
    def set_sentences(self, text):
        """
        Split text into list of sentences using NLTK
        :param text:
        :return:
        """
        # print(text)
        self.sentences = sent_tokenize(text)
        # Remove sentences that are less than 3 words length
        # return none if words are less than 3
        # TODO
        self.sentences = [sen for sen in self.sentences if len(word_tokenize(sen)) > 0]


    @classmethod
    def from_json(cls, data, cluster_map=None):
        return cls(cluster_map=cluster_map, **data)

    def get_topK(self, k):
        """
        Return the k highest scored sentences
        :param k:
        :return:
        """
        print(self.sentences)
        if self.sentences and self.score:
            if k <= len(self.score) and k <= len(self.sentences):
                # print(self.score)
                ind = np.argpartition(np.array(self.score), -k)[-k:]
                ind = np.sort(ind)
                return np.array(self.sentences)[ind]
            else:
                return np.array(self.sentences)

    def __str__(self):
        return "%s, %s, %s, %s" % (self.premises, self.context, self.id
                                   , self.conclusion)

    def __iter__(self):
        return iter(self.sentences)

    def __len__(self):
        return len(self.sentences)


REMAP = {"-LRB-": "(", "-RRB-": ")", "-LCB-": "{", "-RCB-": "}",
         "-LSB-": "[", "-RSB-": "]", "``": '"', "''": '"'}


def clean(x):
    print('test clean')
    return re.sub(
        r"-LRB-|-RRB-|-LCB-|-RCB-|-LSB-|-RSB-|``|''",
        lambda m: REMAP.get(m.group()), x)
