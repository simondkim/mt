
import re
import urllib
import json
import urllib2

class MT:

    dictionary = dict()
    raw_translation = ""

    def __init__(self, text):

        # Reads the text in and translate word by word into English
        for line in open (text, "r"):
            print line
            translation = ""
            words = line.split()
            for word in words:

                while len(word) > 0:

                    # data = urllib2.urlopen('http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q=test&sl=en&tl=en&restrict=pr%2Cde&client=te')
                    #
                    # j = json.load(data)
                    # k = [i for i, j, k in j[1]]
                    # l = json.dumps(k)
                    # print l
                    #
                    # exit()

                    # print word
                    search_url="http://api.wordreference.com/386fd/koen/"+word
                    # print search_url
                    results=urllib.urlopen(search_url)
                    # exit()

                    content=results.read()
                    # print content
                    definitions = re.findall(r'<span class=\'FrW2\'>([ a-zA-Z]*)</span>', content, re.MULTILINE)
                    if not len(definitions) == 0:
                        # print definitions
                        self.dictionary[word] = definitions
                        translation += definitions[0] + " "
                        break

                    word = word[:-1]
                    # print word
            print translation



            # for l in results.readlines():
                #     try:
                #         # print l
                #         m = re.search(r'<span class=\'FrW2\'>(.*)</span>', l)
                #         print m
                #
                #         # # Search the returned HTMl for the hyper-link data for the speciic player.
                #         # # This is mostly string clean up stiff to make the URL string ready for thte next step.
                #         #     split1=l.split('=')
                #         #     first_piece=split1[1].lstrip('"')
                #         #     second_piece=split1[2].split('"')[0]
                #         #     dictionary[word]="http://www.nfl.com"+first_piece+"="+second_piece
                #     except UnicodeDecodeError:
                #         print "Ignoring UnicodeDecodeError"
                # results.close()
                #
                # exit()
            # print words


            # print line
        #     = open (text, "r")
        # data = f.read()
        #
        # for line in data:
        #     print line
            # words = line.split()
            # for word in words:
            #     print word



if __name__ == '__main__':
    text = 'text.txt'

    result = MT(text)
