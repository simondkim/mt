
import re
import urllib
import json
import urllib2

class MT:

    dictionary = dict()
    raw_translation = ""

    def __init__(self, text):

        for line in open (text, "r"):
            words = line.split()
            if len(words) > 1:
                self.dictionary[words[0]] = words[1]
            else:
                self.dictionary[words[0]] = ""

        for paragraph in open ('text.txt', "r"):
            lines = paragraph.split('. ')
            for line in lines:
                trans_line = []
                words = line.split()
                if not len(words) == 0:
                    for word in words:
                        if self.dictionary.has_key(word):
                            if not len(self.dictionary[word]) == 0:
                                trans_line.append(self.dictionary[word])
                    # trans_line.append(".")
                    print trans_line


        # output = ""
        # # Reads the text in and translate word by word into English
        # for line in open (text, "r"):
        #     print line
        #     translation = ""
        #     words = line.split()
        #     for word in words:
        #         output += (word + '\n')
        # print output
        # f = open('output.txt', 'w+')
        # f.write(output)
        # exit()
            #
            #     while len(word) > 0:
            #
            #         # data = urllib2.urlopen('http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q=test&sl=en&tl=en&restrict=pr%2Cde&client=te')
            #         #
            #         # j = json.load(data)
            #         # k = [i for i, j, k in j[1]]
            #         # l = json.dumps(k)
            #         # print l
            #         #
            #         # exit()
            #
            #         # print word
            #         search_url="http://endic.naver.com/popManager.nhn?m=search&query="+word
            #         # print search_url
            #         results=urllib.urlopen(search_url)
            #         # exit()
            #
            #         content=results.read()
            #         # print content
            #         definitions = re.findall(r'<a href="popManager\.nhn\?m=search&query=[a-zA-Z]*">([ a-zA-Z]*)</a>', content, re.MULTILINE)
            #         # print definitions
            #         # exit()
            #
            #         if not len(definitions) == 0:
            #             print definitions
            #             self.dictionary[word] = definitions
            #             translation += definitions[0] + " "
            #             break
            #
            #         word = word[:-1]
            #         # print word
            # print translation


if __name__ == '__main__':
    text = 'output.txt'

    result = MT(text)
