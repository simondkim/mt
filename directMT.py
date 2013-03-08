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
        
        self.states = []
        for line in open('states.txt', 'r'):
            self.states.append(line[:-1])

    def print_dict(self):
        for key in self.dictionary.keys():
            print key, ": ", self.dictionary[key]

    def translate(self, text):
        """Reads text in and stores raw translation"""

        # translating sentence by sentence
        for paragraph in open (text, "r"):
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

        for sentence in self.tagged_sentences:
            words = [tuple[0] for tuple in sentence]
            self.final_output += ' '.join(words)
            self.final_output += "\n"
            print ' '.join(words)
            tags = [tuple[1] for tuple in sentence]
            self.final_output += ' '.join(tags)
            self.final_output += "\n"
            print ' '.join(tags)

            words, tags = result.improve_pos(words, tags)
            words, tags = result.fix_year(words, tags)
            words, tags = result.reorder_location(words, tags)
            words, tags = result.fix_verb_adverb_pos(words, tags)
            words, tags = result.fix_verb_preposition_pos(words, tags)
            words, tags = result.improve_pos2(words, tags)
            words, tags = result.reorder_verb(words, tags)
            words, tags = result.reorder_verb_object(words, tags)

            # print reordered results
            print ' '.join(words)
            print ' '.join(tags)                

    # rule 8: if a noun is followed by verb and preposition,
    # then reorder it so that it is verb + preposition + noun (object)
    def reorder_verb_object(self, words, tags):

        return words, tags

    # rule 6: fixes year by appending 'in' before the word
    def fix_year(self, words, tags):
        i = 0
        while i < len(words):
            if tags[i] == 'CD':
                if len(words[i]) == 4:
                    print "len"
                    words.insert(i, "in")
                    tags.insert(i, "IN")
                    if len(words) - 1 > i + 2:
                        i += 1
            i += 1
        return words, tags

    # rule 4: word is not a noun if it has apostrophe s in it. should be adjective.
    def improve_pos(self, words, tags):
        for i, word in enumerate(words):
            if "'s" in word:
                tags[i] = 'JJ'
        return words, tags

    # rule 7: if a word is adjective and contains 'ed', then is probably a verb past participle,
    # so we fix the pos tag to be VBN for better result.
    # this function has to come after rearranging verb and prepositions.
    def improve_pos2(self, words, tags):
        for i, word in enumerate(words):
            if tags[i] == 'JJ' and "ed" in word:
                if i + 1 < len(tags):
                    if tags[i + 1] == 'IN':
                        tags[i] = 'VBN'
        return words, tags

    # rule 2: verb should go after the adverb if they are adjacent
    def fix_verb_adverb_pos(self, words, tags):
        for i, tag in enumerate(tags):
            if i < len(tags) - 1:
                if (tags[i] == 'VB' or tags[i] == 'VBD' or tags[i] == 'VBG'
                    or tags[i] == 'VBN' or tags[i] == 'VBP' or tags[i] == 'VBZ'):
                    adv_tag = tags[i + 1]
                    adv_word = words[i + 1]
                    if adv_tag == 'RB' or adv_tag == 'RBR' or adv_tag == 'RBS':
                        tags[i + 1] = tags[i]
                        tags[i] = adv_tag
                        words[i + 1] = words[i]
                        words[i] = adv_word
        return words, tags

    # rule 5: verb (VBN) + preposition
    def fix_verb_preposition_pos(self, words, tags):
        for i, tag in enumerate(tags):
            if i < len(tags) - 1:
                if tags[i] == 'IN':
                    verb_tag = tags[i + 1]
                    verb_word = words[i + 1]
                    if verb_tag == 'VBN' or (verb_tag == 'JJ' and "ed" in verb_word):
                        tags[i + 1] = tags[i]
                        tags[i] = verb_tag
                        words[i + 1] = words[i]
                        words[i] = verb_word
        return words, tags

    def reorder_location(self, words, tags):
        if "USA" in words:
            country_index = words.index("USA")
            if country_index < len(words) - 1 and words[country_index + 1] in self.states:
                #state is after country, reorder
                state = words[country_index + 1]
                state_tag = tags[country_index + 1]
                if words[country_index + 2] == "state":
                    del words[country_index + 2]
                    del tags[country_index + 2]
                words[country_index] = state
                words.insert(country_index + 1, ',')
                tags[country_index + 2] = tags[country_index]
                words[country_index + 2] = "USA"
                tags[country_index] = state_tag
                tags.insert(country_index + 1, ',')
        return words, tags

    # rule 1: bring the verb at the end of sentence to the front
    def reorder_verb(self, words, tags):

        if len(words) == 0 or len(tags) == 0:
            return words, tags

        # check if subject is present in the sentence
        subject_start_index = 0
        subject_end_index = 0

        # find the end index of subject
        if tags[0] == 'NNP':
            while subject_end_index < len(tags) - 1:
                if tags[subject_end_index + 1] == 'NNP':
                    subject_end_index += 1
                else:
                    break

        print "subj start index: %d" % subject_start_index
        print "subj end index: %d" % subject_end_index

        # see if verb is present at the end of sentence
        verb_start_index = -1
        verb_end_index = len(tags) - 1
        for tag in reversed(tags):
            if tag == 'VB' or tag == 'VBD' or tag == 'VBG' or tag == 'VBN' or tag == 'VBP' or tag == 'VBZ':
                verb_start_index = tags.index(tag)
                break
        subject_end_index = (0 if subject_end_index == 0 else subject_end_index + 1)
        if verb_start_index == -1:
            return words, tags

    # take out middle part of the sentence before reordering verb
        middle_words = words[subject_end_index: verb_start_index]
        middle_tags = tags[subject_end_index: verb_start_index]

        # move the verb to the front (after subject if subject is present)
        verb_words = words[verb_start_index:verb_end_index]
        words[verb_start_index:verb_end_index] = ''
        words[subject_end_index:subject_end_index] = verb_words
        verb_tags = tags[verb_start_index:verb_end_index]
        tags[verb_start_index:verb_end_index] = ''
        tags[subject_end_index:subject_end_index] = verb_tags

        # print middle_words

        # if not verb_start_index == -1:
        #     middle_words, middle_tags = result.reorder_verb(middle_words, middle_tags)

        # middle_words_start_index = subject_end_index + len(verb_tags)
        # words[middle_words_start_index:len(words)] = ''
        # tags[middle_words_start_index:len(tags)] = ''
        # words[middle_words_start_index:middle_words_start_index] = middle_words
        # tags[middle_words_start_index:middle_words_start_index] = middle_tags

        # print ' '.join(words)
        # print ' '.join(tags)
        return words, tags


def write(self):
        f = open('final2.txt', 'w+')
        f.write(self.final_output)

if __name__ == '__main__':
    dict = 'output.txt'
    text = 'text2.txt'

    result = MT(dict)
    result.translate(text)
    # print result.sentences
    result.tagPOS()
    result.reorder()
    # result.write()
