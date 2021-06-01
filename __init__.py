import json
from snippetGenerator import SnippetGenerator
import os

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

# data_snippets_test = data_snippets_filtered[0:2]
# ---- Test Snippet Generation using different parameters ---

d = 1
# methodSet = ['power','eigen','linear','krylov']
mc_method = 'linear'
aspects_arguments_max = 0
aspects_weights = [0, 0]
arguments = data_snippets_filtered

snippet_generator = SnippetGenerator(arguments, d, mc_method, aspects_arguments_max, aspects_weights)
snippets = snippet_generator.get_snippets(arguments)
count, accuracy = snippet_generator.get_accuracy(arguments, snippets)
print(count, accuracy)
