import json
import os
from .argument import Argument
import pandas as pd


class ContextModelling:
    def __init__(self, aspects_arguments_max, aspects_weights):
        script_dir = os.path.dirname(__file__)
        self.context_data = json.load(open(os.path.join(script_dir, "../data/snippets.txt")))
        self.arguments_df = pd.read_pickle(os.path.join(script_dir, "../../argsme_df_aspect_filtered.pkl"))
        # self.Arguments_df = pd.read_pickle(os.path.join(script_dir, "../data/ArgumentsDatasets.pkl"))
        self.ContextArgsIds = pd.read_pickle(os.path.join(script_dir, "../data/Context_args_list.pkl"))
        self.aspects_args_similar_ids = pd.read_pickle(os.path.join(script_dir, "../data/aspects_args_similar_ids.pkl"))
        self.aspects_arguments_max = aspects_arguments_max
        self.aspects_weights = aspects_weights
        # print(self.Arguments_df.head(2))

    def get_similar_args(self, arg):

        args_ids = []
        context_args_query = []
        for args in self.context_data:
            if args['query'] == arg.context and args['arg_id'] != arg.id:
                args_ids.append(args['arg_id'])
                context_arg = Argument()
                # context_arg.set_sentences(" ".join(args["sentences"]))
                context_arg.sentences = args["sentences"]
                context_args_query.append(context_arg)
        # print(context_args)
        return args_ids, context_args_query

    def retrieve_argumentative_texts(self, arg_id_score):

        context_args_aspects = []
        arguments_df = self.arguments_df

        # take first 50 arguments
        argument_similar_ids_list = list(arg_id_score.keys())
        if len(argument_similar_ids_list) <= self.aspects_arguments_max:
            argument_similar_ids_top = argument_similar_ids_list
        else:
            argument_similar_ids_top = argument_similar_ids_list[:self.aspects_arguments_max]
            # print(type(argument_similar_ids_top))
        # print(len(argument_similar_ids_top))
        argumentative_text_args = []
        for argument_similar_id in argument_similar_ids_top:
            # print(argument_similar_id)
            argumentative_text = arguments_df['text'][argument_similar_id] + arguments_df['conclusion'][
                argument_similar_id]
            # print(ArgumentativeText)
            # print(argument_similar_id)
            args = Argument()
            args.set_sentences(argumentative_text)
            context_args_aspects.append(args)
            argumentative_text_args.append(argumentative_text)

        return context_args_aspects

    def get_aspects_args(self, arg_aspects):
        arguments_df = self.arguments_df
        arg_id_score = dict()
        for index, row in arguments_df.iterrows():
            # x= aspect of another arguments
            other_args_aspect = row['dict_weighted_args_dataset_list_re']
            total_score = 0

            for aspect in arg_aspects:
                # aspect_word_count = len(aspect.split())
                aspect_weight = arg_aspects[aspect]
                if aspect_weight > self.aspects_weights[0]:
                    if aspect in other_args_aspect:
                        if other_args_aspect[aspect] > self.aspects_weights[1]:
                            arg_id = row['arg_id']
                            total_score = total_score + other_args_aspect[aspect]
                            arg_id_score[arg_id] = total_score
                            # other_args_dict[aspect]= round(other_args_dict[aspect],2)

        # print(arg_id_score)
        # sort the arg_id_score score with score of id in descending order
        arg_id_score_sorted = dict(sorted(arg_id_score.items(), key=lambda item: item[1], reverse=True))
        argument_similar_ids_count = len(arg_id_score_sorted)
        print(argument_similar_ids_count)
        print(arg_id_score_sorted)
        context_args_aspects = self.retrieve_argumentative_texts(arg_id_score_sorted)
        return context_args_aspects

    def get_aspects_args2(self, arg_aspects, arg_id):
        # retrieved the pre-saved similar arguments ids from the args.me corpus
        # print(arg_aspects)
        arg_id_score = dict()
        for index, row in self.aspects_args_similar_ids.iterrows():
            if row['id'] == arg_id:
                arg_id_score = row['id_score_dict']
                # print(row['similar_id_count'])
        # print(arg_id_score)
        context_args_aspects = self.retrieve_argumentative_texts(arg_id_score)

        return context_args_aspects

    def get_context_args_same_page(self, context_arg_indices):
        context_args_list = []
        for args_samePage in self.ContextArgsIds['Context_args_list'][context_arg_indices]:
            args = Argument()
            # print(args_samePage)
            args.set_sentences(args_samePage)
            context_args_list.append(args)

        print("arguments in same Pages  ", len(context_args_list))
        return context_args_list
