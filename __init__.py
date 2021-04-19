import json
from snippetGenerator import SnippetGenerator
import os

script_dir = os.path.dirname(__file__)
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

# data_snippets_test = data_snippets_filtered[0:2]
# ---- Test Snippet Generation using different parameters ---

d = 0.15
# methodSet = ['power','eigen','linear','krylov']
mc_method = 'linear'
aspects_arguments_max = 100
aspects_weights = [0, 0]
json_arguments = data_snippets_filtered

snippetGenerator = SnippetGenerator(json_arguments, d, mc_method, aspects_arguments_max, aspects_weights)
snippets = snippetGenerator.get_snippets(json_arguments)

count, accuracy =snippetGenerator.get_accuracy(snippets)
print(count, accuracy)
