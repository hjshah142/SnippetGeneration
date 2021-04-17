import os
import json
from lib.argsrank import ArgsRank
from lib.argument import Argument
from lib.aspectsdetection import AspectsDetection
from lib.contextModelling import ContextModelling

""""
json_argument = {"arguments": 
[{"id": "5",
  "text": "The Supreme Court decided that states can not outlaw abortion because Prohibiting abortion is a crime.},
{"id": "1",
"text": "In 2011 there were about 730,322 abortions reported to the centers for disease control."}]}
with open(os.path.join(script_dir, "data/arguments.txt"), 'w', encoding='utf-8') as f:
    json.dump(json_argument, f, ensure_ascii=False, indent=2)
"""
script_dir = os.path.dirname(__file__)
stored_snippets = json.load(open(os.path.join(script_dir, "data/arguments.txt")), encoding='utf-8')
data_snippets = json.load(open(os.path.join(script_dir, "data/snippets.txt")), encoding='utf-8')

for idx, arguments in enumerate(data_snippets):
    arguments['indices'] = idx
    # print(arguments)

# removing arguments with sentences less then 3
print(len(data_snippets))
count = 0
data_snippets_filtered = []
for argument in data_snippets:

    if len(argument['sentences']) > 2:
        data_snippets_filtered.append(argument)
        count = count + 1

print(count)


def get_snippets(json_arguments):
    # json.loads(json_arguments, encoding='latin1')
    clusters = []
    for argument in json_arguments:
        # print(argument["sentences"])
        arg = Argument()
        argument_text = " ".join(argument["sentences"])
        arg.premises = argument_text
        arg.id = argument["arg_id"]
        arg.aspects = AspectsDetection().get_aspects(argument_text)

        # print(argumentative_text)

        # Argument Text
        arg.context = argument["query"]
        arg.set_sentences(argument_text)
        arg.sentences = argument["sentences"]
        contextModelling = ContextModelling()
        context_args_aspects = contextModelling.get_argumentative_text_args(arg.aspects, arg)
        context_ids, context_args_query = ContextModelling().get_similar_args(arg)
        # print(argumentative_text)
        # print(arg.context_args)
        # print(arg.aspects)
        # print(arg.sentences)
        # print(context_args)
        # arg_cluster = context_args
        indices = argument["indices"]
        print('index', indices)
        context_args_samePage = ContextModelling().get_context_args_samePage(indices)
        # print(context_args_samePage)
        arg_cluster = context_args_aspects + context_args_query + context_args_samePage
        # arg_cluster = arg_cluster.insert(0,arg)
        print(len(arg_cluster))
        clusters.append(arg_cluster)

    print(len(clusters))
    print('generated snippets...')
    snippet_gen_app = ArgsRank()
    snippets_generated = snippet_gen_app.generate_snippet(clusters)
    return snippets_generated


snippets = get_snippets(data_snippets_filtered)

with open(os.path.join(script_dir, "data/snippetsGenerated.txt"), 'w', encoding='utf-8') as f:
    json.dump(snippets, f, indent=2)
# print(snippets)
print('snippets generated File is created ')
