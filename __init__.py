import json
import os
from snippetGenerator import SnippetGenerator

script_dir = os.path.dirname(__file__)
data_snippets = json.load(open(os.path.join(script_dir, "data/snippets.txt")), encoding='utf-8')

for idx, arguments in enumerate(data_snippets):
    arguments['index'] = idx
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

dev_args_set = ['feminism', 'death_penalty', 'brexit']
test_args = []
dev_args = []
for args in data_snippets_filtered:
    if args['query'] in dev_args_set:
        dev_args.append(args)
    else:
        test_args.append(args)
# Test Snippet Generation using different parameters ---

d = 0

# methodSet = ['power','eigen','linear','krylov']
argumentative_score_methods = ['discourse_claim_markers', 'argument_score', 'claim_score', 'hybrid_score']
mc_method = 'eigen'
aspects_arguments_max = 200
aspects_weights = [0, 0]
arguments = test_args
# argument_context =[1,1,1]
# argument_context_clusters = ['query',same page','aspect']
argument_context = [1, 0, 1]
argumentative_score_method = argumentative_score_methods[0]


snippet_generator = SnippetGenerator(arguments, d, mc_method, aspects_arguments_max, aspects_weights,
                                     argument_context, argumentative_score_method)
snippets = snippet_generator.get_snippets(arguments)
count, accuracy = snippet_generator.get_accuracy(arguments, snippets)
print(count, accuracy)
