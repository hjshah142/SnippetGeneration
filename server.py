import os

from flask import Flask, url_for
from flask import json
from flask import request
from flask import Response
from flask import g

import json
from tensorflow import keras

from lib import argsrank
from lib.argument import Argument


json_argument = {"arguments": [{"id": "5",
                                "text": "The Supreme Court decided that states can not outlaw abortion because Prohibiting abortion is a violation of the 14th Amendment, according to the Court, and the constitution.. Outlawing abortion is taking away a human right given to women.. in reality, a fetus is just a bunch of cells.. It has not fully developed any vital organs like lungs.. This means that an abortion is not murder, it is just killing of cells in the wound.. If the child has no organs developed that would be vital for the baby to survive outside the wound, than having an abortion is not murder."},
                               {"id": "1",
                                "text": "In 2011 there were about 730,322 abortions reported to the centers for disease control.. There are about 1.7% of abortion of womens ages from 15-44 each year.. Women who already had abortion earlier in there life time have abortion again.. At the age of 45 a women will have at least one abortion.. By the 12th week of pregnancies 88.7% of women have abortion.. In the U.S. black women are 3.3 times likely to have an abortion than white women."}]}

script_dir = os.path.dirname(__file__)
stored_snippets = json.load(open(os.path.join(script_dir, "data/snippets.txt")))
print(len(stored_snippets))
snippet_gen_app = argsrank.ArgsRank()









def get_snippets(json_arguments):
    cluster = []
    #json.loads(json_arguments, encoding='latin1')
    json_arguments = json_arguments['arguments']
    for argument in json_arguments:
        print(argument["text"])
        arg = Argument()
        arg.premises = [{"text": argument["text"]}]
        arg.id = argument["id"]
        arg.set_sentences(argument["text"])
        cluster.append(arg)

    print(cluster)
    print('generated snippets...')
    snippets = snippet_gen_app.generate_snippet(cluster)

    return snippets

snippets= get_snippets(json_argument)

print(snippets)
