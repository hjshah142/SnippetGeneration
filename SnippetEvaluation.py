from pathlib import Path
import os
import json
import pandas as pd

script_dir = os.path.dirname(Path().absolute())
generated_snippets = json.load(open(os.path.join(script_dir, "ExtractiveSnipp/data/snippetsGenerated.txt")))
data_snippets = json.load(open(os.path.join(script_dir, "ExtractiveSnipp/data/snippets.txt")))

arg_aspects = []
for arguments in generated_snippets:
    arg_aspects.append(arguments['aspects'])
len(arg_aspects)

count = 0
data_snippets_filtered = []
for argument in data_snippets:

    # print(argument['sentences'])
    if len(argument['sentences']) > 2:
        data_snippets_filtered.append(argument)
        count = count + 1

data_snippets_df = pd.json_normalize(data_snippets_filtered)
generated_snippets_df = pd.json_normalize(generated_snippets)
generated_snippets_df = generated_snippets_df = generated_snippets_df.iloc[:, 0:3]

generated_snippets_df.insert(2, 'generated_snippets', data_snippets_df['snippet'])

count = 0
for index, row in generated_snippets_df.iterrows():
    snippets_detected = row['generated_snippets']
    snippets_answer = row['snippets-text']
    # print(other_args_dict)
    for x in snippets_answer:
        for y in snippets_detected:
            # print(x)
            # print(y)
            # print("-------------")
            if x == y:
                count = count + 1
                # print('match')

print(count)
accuracy = (100.0 * count) / (2 * len(generated_snippets))
print(accuracy)
