import os
import json
from lib.argsrank import ArgsRank
from lib.argument import Argument
from lib.aspectsdetection import AspectsDetection
from lib.contextModelling import ContextModelling
import pandas as pd


class SnippetGenerator:

    def __init__(self, json_arguments, d, mc_method, aspects_arguments_max, aspects_weights):
        self.d = d
        # methodSet = ['power','eigen','linear','krylov']
        self.mc_method = mc_method
        self.aspects_arguments_max = aspects_arguments_max
        self.aspects_weights = aspects_weights
        self.json_arguments = json_arguments
        # script_dir = os.path.dirname(__file__)
        # snippets = self.get_snippets(self.json_arguments)

    def get_snippets(self, json_arguments):
        # json.loads(json_arguments, encoding='latin1')
        clusters = []
        for argument in json_arguments:
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
            context_args_aspects = contextModelling.get_aspects_args(arg.aspects)
            context_ids, context_args_query = contextModelling.get_similar_args(arg)
            arg.indices = argument["indices"]
            print('index', arg.indices)
            context_args_samePage = contextModelling.get_context_args_samePage(arg.indices)
            args_object = [arg]
            # print(context_args_samePage)
            arg_cluster = args_object + context_args_aspects + context_args_query
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

    def get_accuracy(self,generated_snippets):
        data_snippets_df = pd.json_normalize(self.json_arguments)
        generated_snippets_df = pd.json_normalize(generated_snippets)
        generated_snippets_df = generated_snippets_df.iloc[:, 0:3]

        generated_snippets_df.insert(2, 'generated_snippets', data_snippets_df['snippet'])

        count = 0
        for index, row in generated_snippets_df.iterrows():
            snippets_detected = row['generated_snippets']
            snippets_answer = row['snippets-text']
            # print(other_args_dict)
            for x in snippets_answer:
                for y in snippets_detected:
                    # print(x)
                    # print(y)
                    # print("-------------")
                    if x == y:
                        count = count + 1
                        # print('match')

        print(count)
        accuracy = (100.0 * count) / (2 * len(generated_snippets))
        print(accuracy)
        return count, accuracy

