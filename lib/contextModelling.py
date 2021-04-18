import json
import os
from .argument import Argument
import pandas as pd


class ContextModelling:
    def __init__(self, aspects_arguments_max):
        script_dir = os.path.dirname(__file__)
        self.context_data = json.load(open(os.path.join(script_dir, "../data/snippets.txt")))
        self.Arguments_df = pd.read_pickle(os.path.join(script_dir, "../data/ArgumentsDatasets.pkl"))
        self.ContextArgsIds = pd.read_pickle(os.path.join(script_dir, "../data/Context_args_list.pkl"))
        self.aspects_arguments_max = aspects_arguments_max
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
        Arguments_df = self.Arguments_df

        # take first 50 arguments
        argument_similar_ids_list = list(arg_id_score.keys())
        if len(argument_similar_ids_list) <= self.aspects_arguments_max:
            argument_similar_ids_top = argument_similar_ids_list
        else:
            argument_similar_ids_top = argument_similar_ids_list[:self.aspects_arguments_max]
            # print(type(argument_similar_ids_top))
        print(len(argument_similar_ids_top))
        ArgumentativeText_args = []
        for argument_similar_id in argument_similar_ids_top:
            # print(argument_similar_id)
            ArgumentativeText = Arguments_df['text'][argument_similar_id] + Arguments_df['conclusion'][
                argument_similar_id]

            Args = Argument()
            Args.set_sentences(ArgumentativeText)
            context_args_aspects.append(Args)
            ArgumentativeText_args.append(ArgumentativeText)

        return context_args_aspects

    def get_aspects_args(self, arg_aspects):

        # print(arg_aspects)
        score = 0
        arg_id_score = dict()
        # context_args_aspects = [arg_object]

        for aspect in arg_aspects:
            # aspect_word_count = len(aspect.split())
            aspect_weight = arg_aspects[aspect]
            if aspect_weight >= 0:

                for index, row in self.Arguments_df.iterrows():
                    # x= dict object of aspect detected
                    other_args_dict = row['dict_weighted_args_dataset_list_re']

                    if aspect in other_args_dict and other_args_dict[aspect] > 0:
                        arg_id = row['arg_id']
                        if arg_id in arg_id_score:
                            # print('match found')
                            # print(other_args_dict[aspect])
                            arg_id_score[arg_id] = score + other_args_dict[aspect]
                            # other_args_dict[aspect]= round(other_args_dict[aspect],2)
                        else:

                            score = other_args_dict[aspect]
                            arg_id_score[arg_id] = score

        arg_id_score = dict(sorted(arg_id_score.items(), key=lambda item: item[1], reverse=True))

        # print(arg_id_score)
        # argument_similar_ids.append(arg_id_score)
        argument_similar_ids_count = len(arg_id_score)
        print(argument_similar_ids_count)
        context_args_aspects = self.retrieve_argumentative_texts(arg_id_score)

        return context_args_aspects

    def get_context_args_samePage(self, context_arg_indices):
        context_args_list = []
        for args_samePage in self.ContextArgsIds['Context_args_list'][context_arg_indices]:
            args = Argument()
            # print(args_samePage)
            args.set_sentences(args_samePage)
            context_args_list.append(args)

        print("arguments in same Pages  ", len(context_args_list))
        return context_args_list
