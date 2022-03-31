import re
import string


class WordExtractor:

    def __init__(self, text: str):
        self.text = text
        self.words = {}

    def extract(self, global_word_set=None, doc_id=-1):
        pos = 0
        word_list = self.text.split()
        for word in word_list:
            word = word.lower()
            word = word.lstrip('0123456789.- ')
            s = re.sub(r'^[^a-z]+', '', word)
            extracted = s.translate(str.maketrans('', '', string.punctuation))
            if len(extracted) > 0:
                if extracted in self.words:
                    self.words[extracted].append(pos)
                else:
                    if global_word_set is not None:
                        if extracted not in global_word_set:
                            global_word_set[extracted] = set([doc_id])
                        else:
                            global_word_set[extracted].add(doc_id)
                    self.words[extracted] = [pos]
            pos += 1
        return self.words
