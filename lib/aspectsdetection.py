import re
import os


class AspectsDetection:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, "../data/WikiAspects.txt"), encoding='utf8')
        #  Wikipedia list of the controversial issues derived from the work of ( Ajjour et al.,2008) [4].
        self.aspect_list = f.read().lower().split('\n')

    def get_aspects(self, text):
        """
         Conducts a full-text search of every aspect in the ' Wikipedia aspects list of the controversial issues'
         to the given argument. Uses the regular expression method to find the list of the aspects covered by
         given argument.
        :param text: text of an argument
        :return: list of aspects covered by the given arguments with zhe normalised weight of every aspect
        """
        text = text.lower()

        aspect_detected = {}
        for aspect in self.aspect_list:
            if re.search(r"\b" + re.escape(aspect) + r"\b", text):
                aspect_count = len(re.findall(r"\b" + re.escape(aspect) + r"\b", text))
                # print(aspect_count)
                aspect_detected[aspect] = aspect_count

        print(aspect_detected)
        # to calculate  the normalised weight of every aspect in the aspect list for the argument
        aspects_dict = {k: v / total for total in (sum(aspect_detected.values()),)
                        for k, v in aspect_detected.items()}
        print(aspects_dict)
        return aspects_dict
