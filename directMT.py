import re
import urllib
import json
import urllib2

class MT:

    dictionary = dict()
    raw_translation = ""

    def __init__(self, text):

        # Reads the dict in and stores internally
        for line in open (text, "r"):
            words = line.split()
            self.dictionary[words[0]] = words[1]

    def print_dict(self):
        for key in self.dictionary.keys():
            print key, ": ", self.dictionary[key]

    def translate(self, text):
        """Reads text in and stores raw translation"""

        for line in open (text, 'r'):
            words = line.split()
            for word in words:
                #TODO: handle punctuation by directly translating
                if self.dictionary.get(word):
                    self.raw_translation += self.dictionary[word] + " "

    def tagPOS(self):
        """Runs Stanford POS tagger on raw translation"""
        #TODO
        pass

if __name__ == '__main__':
    dict = 'dict.txt'
    text = 'text.txt'

    result = MT(dict)
    result.translate(text)
