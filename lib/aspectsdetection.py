import re
import os


class AspectsDetection:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, "../data/WikiAspects.txt"), encoding='utf8')
        self.aspect_list = f.read().lower().split('\n')

    def get_aspects(self, text):
        text = text.lower()

        aspect_detected = {}
        for aspect in self.aspect_list:
            if re.search(r"\b" + re.escape(aspect) + r"\b", text):
                aspect_count = len(re.findall(r"\b" + re.escape(aspect) + r"\b", text))
                # print(aspect_count)
                aspect_detected[aspect] = aspect_count

        print(aspect_detected)
        aspects_dict = {k: v / total for total in (sum(aspect_detected.values()),)
                        for k, v in aspect_detected.items()}
        print(aspects_dict)
        return aspects_dict
