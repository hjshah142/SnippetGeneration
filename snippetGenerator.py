import os
import json
from lib.argsrank import ArgsRank
from lib.argument import Argument
from lib.aspectsdetection import AspectsDetection
from lib.contextModelling import ContextModelling
import pandas as pd


class SnippetGenerator:

    def __init__(self, arguments, d, mc_method, aspects_arguments_max, aspects_weights):
        self.d = d
        # methodSet = ['power','eigen','linear','krylov']
        self.mc_method = mc_method
        self.aspects_arguments_max = aspects_arguments_max
        self.aspects_weights = aspects_weights
        self.arguments = arguments

    def get_snippets(self, arguments):
        # json.loads(json_arguments, encoding='latin1')
        clusters = []
        for argument in arguments:
            # print(argument["sentences"])
            arg = Argument()
            argument_text = " ".join(argument["sentences"])
            arg.premises = argument_text
            arg.id = argument["arg_id"]
            arg.aspects = AspectsDetection().get_aspects(argument_text)
            arg.context = argument["query"]
            # arg.set_sentences(argument_text)
            arg.sentences = argument["sentences"]
            contextModelling = ContextModelling(self.aspects_arguments_max, self.aspects_weights)
            # context_args_aspects = contextModelling.get_aspects_args(arg.aspects)
            context_args_aspects = contextModelling.get_aspects_args2(arg.aspects, arg.id)
            context_ids, context_args_query = contextModelling.get_similar_args(arg)
            arg.index = argument["index"]
            print('index', arg.index)
            # context_args_samePage = contextModelling.get_context_args_same_page(arg.indices)
            args_object = [arg]
            # print(context_args_samePage)
            arg_cluster = args_object + context_args_aspects + context_args_query
            # arg_cluster = args_object
            # arg_cluster = arg_cluster.insert(0,arg)
            print(len(arg_cluster))
            clusters.append(arg_cluster)

        print(len(clusters))
        print('generated snippets...')
        snippet_gen_app = ArgsRank(self.d, self.mc_method)
        snippets_generated = snippet_gen_app.generate_snippet(clusters)
        script_dir = os.path.dirname(__file__)
        # snippets = self.get_snippets(self.json_arguments)
        with open(os.path.join(script_dir, "data/snippetsGenerated.txt"), 'w', encoding='utf-8') as f:
            json.dump(snippets_generated, f, indent=2)
        # print(snippets)
        print('snippets generated File is created ')
        return snippets_generated

    def get_accuracy(self, data_snippets_filtered, snippets):

        count = 0
        for sentence_index in range(0, len(data_snippets_filtered), 1):
            actual_snippets = data_snippets_filtered[sentence_index]['snippet']
            generated_snippets = snippets[sentence_index]['snippets-text']

            for x in actual_snippets:
                for y in generated_snippets:
                    if x == y:
                        count += 1

        print(count)
        accuracy = (100.0 * count) / (2 * len(data_snippets_filtered))
        print(accuracy)
        return count, accuracy
