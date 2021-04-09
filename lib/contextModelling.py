import json
import os
from .argument import Argument


class ContextModelling:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.context_data = json.load(open(os.path.join(script_dir, "../data/snippets.txt")))

    def get_similar_args(self, arg):

        args_ids = []
        context_args = [arg]
        for args in self.context_data:
            if args['query'] == arg.context and args['arg_id'] != arg.id:
                args_ids.append(args['arg_id'])
                context_arg = Argument()
                context_arg.set_sentences(" ".join(args["sentences"]))
                #context_args.append(context_arg)
        # print(context_args)
        return args_ids, context_args
