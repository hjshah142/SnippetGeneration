import os

"""
from flask import Flask, url_for
from flask import json
from flask import request
from flask import Response
from flask import g
"""
import json
from lib.argsrank import ArgsRank
from lib.argument import Argument
from lib.aspectsdetection import AspectsDetection
from lib.contextModelling import ContextModelling

""""
json_argument = {"arguments": [{"id": "5",
                                "text": "The Supreme Court decided that states can not outlaw abortion because Prohibiting abortion is a violation of the 14th Amendment, according to the Court, and the constitution.. Outlawing abortion is taking away a human right given to women.. in reality, a fetus is just a bunch of cells.. It has not fully developed any vital organs like lungs.. This means that an abortion is not murder, it is just killing of cells in the wound.. If the child has no organs developed that would be vital for the baby to survive outside the wound, than having an abortion is not murder."},
                               {"id": "1",
                                "text": "In 2011 there were about 730,322 abortions reported to the centers for disease control.. There are about 1.7% of abortion of womens ages from 15-44 each year.. Women who already had abortion earlier in there life time have abortion again.. At the age of 45 a women will have at least one abortion.. By the 12th week of pregnancies 88.7% of women have abortion.. In the U.S. black women are 3.3 times likely to have an abortion than white women."}]}

with open(os.path.join(script_dir, "data/arguments.txt"), 'w', encoding='utf-8') as f:
    json.dump(json_argument, f, ensure_ascii=False, indent=2)


"""
script_dir = os.path.dirname(__file__)
stored_snippets = json.load(open(os.path.join(script_dir, "data/arguments.txt")))
data_snippets = json.load(open(os.path.join(script_dir, "data/snippets.txt")))


# print(len(stored_snippets))


def get_snippets(json_arguments):
    cluster = []
    # json.loads(json_arguments, encoding='latin1')

    for argument in json_arguments:
        # print(argument["sentences"])
        arg = Argument()
        argument_text = " ".join(argument["sentences"])
        arg.premises = argument_text
        arg.id = argument["arg_id"]
        arg.aspects = AspectsDetection().get_aspects(argument_text)
        # Argument Text
        arg.context = argument["query"]
        arg.set_sentences(argument_text)
        context_ids, context_args = ContextModelling().get_similar_args(arg.context, arg.id)
        # print(context_ids, "      ", context_args)
        arg.context_args = context_args
        # print(arg.context_args)
        # print(arg.aspects)
        # print(arg.sentences)
        cluster.append(arg)
    print(len(cluster))
    # print(cluster)
    print('generated snippets...')
    snippets = snippet_gen_app.generate_snippet(cluster)
    return snippets


snippet_gen_app = ArgsRank()
snippets = get_snippets(data_snippets)


with open(os.path.join(script_dir, "data/snippetsGenerated.txt"), 'w', encoding='utf-8') as f:
    json.dump(snippets, f, indent=2)
# print(snippets)
print('snippets generated File is created ')