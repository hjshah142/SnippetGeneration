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
for argument_x in data_snippets:

    if len(argument_x['sentences']) > 2:
        data_snippets_filtered.append(argument_x)
        count = count + 1

print(count)


d = 0
# methodSet = ['power','eigen','linear','krylov']
mc_method = 'linear'
aspects_arguments_max = 100
aspects_weights = [0,0]


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
        arg.context = argument["query"]
        # arg.set_sentences(argument_text)
        arg.sentences = argument["sentences"]
        contextModelling = ContextModelling(aspects_arguments_max, aspects_weights)
        context_args_aspects = contextModelling.get_aspects_args(arg.aspects)
       #  context_args_aspects = contextModelling.get_aspects_args2(arg.aspects, arg.id)
        context_ids, context_args_query = contextModelling.get_similar_args(arg)
        arg.indices = argument["indices"]
        print('index', arg.indices)
        context_args_samePage = contextModelling.get_context_args_same_page(arg.indices)
        args_object = [arg]
        # print(context_args_samePage)
        arg_cluster = args_object + context_args_aspects + context_args_query
        # arg_cluster = arg_cluster.insert(0,arg)
        print(len(arg_cluster))
        clusters.append(arg_cluster)

    print(len(clusters))
    print('generated snippets...')
    snippet_gen_app = ArgsRank(d, mc_method)
    snippets_generated = snippet_gen_app.generate_snippet(clusters)
    return snippets_generated


data_snippets_test = data_snippets_filtered[0:2]
snippets = get_snippets(data_snippets_filtered)

with open(os.path.join(script_dir, "data/snippetsGenerated.txt"), 'w', encoding='utf-8') as f:
    json.dump(snippets, f, indent=2)
# print(snippets)
print('snippets generated File is created ')

