import os
import json


class ContextModelling:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.context_data = json.load(open(os.path.join(script_dir, "../data/snippets.txt")))

    def get_similar_args(self, context, id):

        args_ids = []
        context_args_text = []
        for args in self.context_data:
            if args['query'] == context  and args['arg_id'] != id:
                args_ids.append(args['arg_id'])
                for sentences in args["sentences"]:
                    context_args_text.append(sentences)

        return args_ids, context_args_text
