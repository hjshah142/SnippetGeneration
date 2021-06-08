import os
import json
from lib.argsrank import ArgsRank
from lib.argument import Argument
from lib.aspectsdetection import AspectsDetection
from lib.contextModelling import ContextModelling


class SnippetGenerator:

    def __init__(self, arguments, d, mc_method, aspects_arguments_max, aspects_weights,
                 argument_context=None, argumentative_score_method=None):
        self.d = d
        # methodSet = ['power','eigen','linear','krylov']
        self.mc_method = mc_method
        self.aspects_arguments_max = aspects_arguments_max
        self.aspects_weights = aspects_weights
        self.arguments = arguments

        if argument_context is None:

            argumentative_score_method = [True, True, True]
        self.argument_context = argument_context

        # argumentatve_score_methods = ['argument_score','claim_score','hybrid_score']
        if argumentative_score_method is None:

            argumentative_score_method = "discourse_claim_markers"
        self.argumentative_score_method = argumentative_score_method

    def get_snippets(self, arguments):
        # json.loads(json_arguments, encoding='latin1')
        clusters = []

        context_modelling = ContextModelling(self.aspects_arguments_max, self.aspects_weights)
        aspect_detection = AspectsDetection()
        print("Context_array", self.argument_context)
        snippet_gen_app = ArgsRank(self.d, self.mc_method, self.argumentative_score_method)
        print("aspects_weights:", self.aspects_weights, "aspects_arguments_max", self.aspects_arguments_max)

        for argument in arguments:
            arg = Argument()
            argument_text = " ".join(argument["sentences"])
            arg.premises = argument_text
            arg.id = argument["arg_id"]
            arg.aspects = aspect_detection.get_aspects(argument_text)
            arg.context = argument["query"]
            arg.index = argument["index"]
            # arg.set_sentences(argument_text)
            arg.sentences = argument["sentences"]
            args_object = [arg]
            arg_cluster = args_object
            # argument_context_clusters = ['query',same page','aspect'] default [1,1,1]
            if self.argument_context[0]:
                context_ids, context_args_query = context_modelling.get_similar_args(arg)
                arg_cluster = arg_cluster + context_args_query
            if self.argument_context[1]:
                context_args_same_page = context_modelling.get_context_args_same_page(arg.index)
                arg_cluster = arg_cluster + context_args_same_page
            if self.argument_context[2]:
                context_args_aspects = context_modelling.get_aspects_args2(arg.aspects, arg.id)
                arg_cluster = arg_cluster + context_args_aspects

            # arg_cluster = args_object + context_args_aspects + context_args_query
            # arg_cluster = args_object
            # arg_cluster = arg_cluster.insert(0,arg)
            # print(len(arg_cluster))
            clusters.append(arg_cluster)

        # print(len(clusters))
        # print('generated snippets...')

        snippets_generated = snippet_gen_app.generate_snippet(clusters)
        script_dir = os.path.dirname(__file__)
        # snippets = self.get_snippets(self.json_arguments)
        with open(os.path.join(script_dir, "data/snippetsGenerated.txt"), 'w', encoding='utf-8') as f:
            json.dump(snippets_generated, f, indent=2)
        print('snippets generated File created ')
        return snippets_generated

    def get_accuracy(self, arguments_filtered, snippets):

        count = 0
        for sentence_index in range(0, len(arguments_filtered), 1):
            actual_snippets = arguments_filtered[sentence_index]['snippet']
            generated_snippets = snippets[sentence_index]['snippets-text']

            for x in actual_snippets:
                for y in generated_snippets:
                    if x == y:
                        count += 0.5

        print(count)
        accuracy = (100.0 * count) / len(arguments_filtered)
        print("Accuracy ", accuracy)
        return count, accuracy
