import re
import urllib
import json
import urllib2
from nltk.tag.stanford import POSTagger

class MT:

    final_output = ""
    dictionary = dict()
    raw_translation = ""
    st = POSTagger('stanford-postagger/models/english-bidirectional-distsim.tagger', path_to_jar='stanford-postagger/stanford-postagger.jar')
    sentences = []
    tagged_sentences = []

    def __init__(self, text):

        # Reads the dict in and stores internally
        for line in open (text, "r"):
            words = line.split()
            if len(words) > 1:
                self.dictionary[words[0]] = words[1:]

    def print_dict(self):
        for key in self.dictionary.keys():
            print key, ": ", self.dictionary[key]

    def translate(self, text):
        """Reads text in and stores raw translation"""

        # translating sentence by sentence
        for paragraph in open ('text.txt', "r"):
            paragraph = paragraph[:-2]
            sentences = paragraph.split('. ')
            for sentence in sentences:
                sentence = re.sub(',', ' , ', sentence)
                sentence = re.sub('\(', ' ( ', sentence)
                sentence = re.sub('\)', ' ) ', sentence)
                sentence = re.sub("'",  " ' ", sentence)
                translated = []
                words = sentence.split()
                if not len(words) == 0:
                    for word in words:
                        # print word
                        if self.dictionary.has_key(word):
                            if not len(word) == 0:
                                # print self.dictionary[word]
                                for translated_word in self.dictionary[word]:
                                    translated.append(translated_word)
                    translated.append(".")
                    self.sentences.append(translated)

    def tagPOS(self):
        """Runs Stanford POS tagger on raw translation"""
        for sentence in self.sentences:
            tagged = self.st.tag(sentence)
            self.tagged_sentences.append(tagged)

    def reorder(self):
        count = 0
        for sentence in self.tagged_sentences:
            self.final_output += ' '.join(self.sentences[count])
            self.final_output += "\n"
            print ' '.join(self.sentences[count])
            tags = [tuple[1] for tuple in sentence]
            self.final_output += ' '.join(tags)
            self.final_output += "\n"
            print ' '.join(tags)
            count += 1

    def write(self):
        f = open('final.txt', 'w+')
        f.write(self.final_output)

if __name__ == '__main__':
    dict = 'output.txt'
    text = 'text.txt'

    result = MT(dict)
    result.translate(text)
    # print result.sentences
    result.tagPOS()
    result.reorder()
    result.write()
