import re
import os

class AspectsDetection:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        print(script_dir)
        f = open(os.path.join(script_dir, "../data/WikiAspects.txt"),encoding='utf8')
        self.aspect_list = f.read().lower().split('\n')

    def get_aspects(self,text):
        total_aspects = []
        aspect_dict_list = []

        aspect_detected = {}
        for aspect in self.aspect_list:
            if re.search(r"\b" + re.escape(aspect) + r"\b", text):
                total_aspects.append(aspect)
                print(aspect)
                aspect_count = len(re.findall(r"\b" + re.escape(aspect) + r"\b", text))
                # print(aspect_count)
                aspect_detected[aspect] = aspect_count

        aspect_dict_list.append(aspect_detected)

        return aspect_dict_list
