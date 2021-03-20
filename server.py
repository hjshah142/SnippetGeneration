import os

"""
from flask import Flask, url_for
from flask import json
from flask import request
from flask import Response
from flask import g
"""
import json
from lib import argsrank
from lib.argument import Argument
from lib.aspectsdetection import AspectsDetection

json_argument = {"arguments": [{"id": "5",
                                "text": "The Supreme Court decided that states can not outlaw abortion because Prohibiting abortion is a violation of the 14th Amendment, according to the Court, and the constitution.. Outlawing abortion is taking away a human right given to women.. in reality, a fetus is just a bunch of cells.. It has not fully developed any vital organs like lungs.. This means that an abortion is not murder, it is just killing of cells in the wound.. If the child has no organs developed that would be vital for the baby to survive outside the wound, than having an abortion is not murder."},
                               {"id": "1",
                                "text": "In 2011 there were about 730,322 abortions reported to the centers for disease control.. There are about 1.7% of abortion of womens ages from 15-44 each year.. Women who already had abortion earlier in there life time have abortion again.. At the age of 45 a women will have at least one abortion.. By the 12th week of pregnancies 88.7% of women have abortion.. In the U.S. black women are 3.3 times likely to have an abortion than white women."}]}

script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, "data/arguments.txt"), 'w', encoding='utf-8') as f:
    json.dump(json_argument, f, ensure_ascii=False, indent=2)


stored_snippets = json.load(open(os.path.join(script_dir, "data/arguments.txt")))
print(len(stored_snippets))


def get_snippets(json_arguments= stored_snippets):
    cluster = []
    # json.loads(json_arguments, encoding='latin1')
    json_arguments = json_arguments['arguments']
    print(json_arguments)
    for argument in json_arguments:
        print(argument["text"])
        arg = Argument()
        aspects = AspectsDetection().get_aspects(argument["text"])
        print(aspects)

        arg.premises = [{"text": argument["text"]}]
        arg.id = argument["id"]
        # Argument Text

        # Argument Sentence tokenization
        arg.set_sentences(argument["text"])
        cluster.append(arg)
    print(len(cluster))
    # print(cluster)
    print('generated snippets...')
    snippets = snippet_gen_app.generate_snippet(cluster)
    return snippets


snippet_gen_app = argsrank.ArgsRank()
snippets = get_snippets(json_argument)

print(snippets)

with open(os.path.join(script_dir, "data/snippetsGenerated.txt"), 'w', encoding='utf-8') as f:
    json.dump(snippets, f, ensure_ascii=False, indent=2)
