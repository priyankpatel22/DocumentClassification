'''
Builds the dictionaries of words based on the 100 documents gathered.

The first('raw') dictionary is of all the unique words that are not in the stopword list and all words that do not have a series
of special characters.

The second dictionary is built by taking the raw dictionary and removing all the post-fixes from the words.

Needs ntlk to installed to run. See: http://www.nltk.org/

'''
# -*- coding: utf-8 -*-
import os
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
import csv

rawDictionary = set()

#processes the text in all the documents so that the analysis can be completed
def processText(full_stop_set,path ):
    for filename in os.listdir(path):
        #hidden file in osx filesytems. if it's present in the directory, then it skips the file
        if filename == ".DS_Store":
            continue
        
        #open and read the file
        raw = open(path + filename).read()

        #first pass on the words. creates a tokens based on spaces in the text, converts to lower case and removes anything in the stop set (words, chars, unicode, etc..)
        #this step is necessary to preprocess the text so nltk does not crash
        filtered_file_words = [w for w in raw.split() if not w.lower() in full_stop_set]
        
        #recombines the text in and passes to ntlk to do a proper tokenize
        tokens = word_tokenize(str(filtered_file_words).rstrip())
        
        #during the rsplit process above, it inserts a ' char, this removes it
        t = [x.replace("'", "") for x in tokens]
        
        #removes a lot more words with unicode chars in the middle of the word, and words with chars that aren't needed in the dictionary
        t_final = [(x.lower()) for x in t if (x not in full_stop_set) and (len(x) > 2) and (x.find('\\x') == -1) and (x.find('/') == -1) and (x.find('\\') == -1) and (x.find('.') == -1) and (x.find('*') != 0) and (x.find('-') != 0)and (x.find('+') != 0 and (x.find(':') == -1))]
        [rawDictionary.add(x.encode('utf-8')) for x in set(t_final) ]
        
    return set(rawDictionary)



def removePostFix(rawDictionary_full):
    leaves = ["s", "es", "ed", "er", "ly", "ing"]
    
    finalDictionary = set()
    for word in rawDictionary_full:
        for leaf in leaves:
            if word[-len(leaf):] == leaf:
                  finalDictionary.add(word[:-len(leaf)])
            
    return finalDictionary




def main():
    #directory set up
    script_dir = os.path.dirname(__file__).split('Scripts')[0]
    file_path = os.path.join(script_dir, "Documents/")
    stop_word_path = os.path.join(script_dir, "Stopwords/")
    dicionary_path = os.path.join(script_dir, "Dictionaries/")
    
    #creates a stoplist of of words and characters to be removed from the dictionaries.
    punctuation = set(['.', '?', '!', ',', '$', ':', ';', '(',')','-',"`",'\'','"','>>','|','."',',"', '[',']', '``', '...'])
    stop_words = set([line.strip() for line in open(stop_word_path+'stopwords.txt', 'rU')])
    other_words = set([line.strip() for line in open(stop_word_path+'unicode.txt', 'rU')])
    ingorelist_words = set([line.strip() for line in open(stop_word_path+'ignorelist.txt', 'rU')])
    unicode_chars = set(['4\\x966',u',\u201d',u'\u2019',u'\u2014',u'\u201c',u'.\u201d',u'\ufffd', u',\ufffd', u'.\ufffd'])
    full_stop_set = set(nltk.corpus.stopwords.words('english')) | punctuation | unicode_chars | other_words | stop_words | ingorelist_words
    

    #build food dictionary
    path = file_path+"Food/"
    rawDictionary_food = processText(full_stop_set,path)
    
    #build company dictionary
    path = file_path+"Company/"
    rawDictionary_company = processText(full_stop_set,path)
    
    #merge the company and food dictionaries togeother to create the 'raw' dictionary
    rawDictionary_full = set(rawDictionary_food.union(rawDictionary_company))
    #print sorted(rawDictionary_full)
    

    
    finalDictionary = removePostFix(rawDictionary_full)
    
    
    
    #write the dictionaries to file
    with open(dicionary_path + 'rawDictionary_full3.txt', 'wb') as f:
        for w in sorted(rawDictionary_full):
            f.write(w+"\n")
        
    f.close()
    
    
    with open(dicionary_path + 'lemmDictionary_full3.txt', 'wb') as g:
        for w in sorted(finalDictionary):
            g.write(w+"\n")
        
    g.close()
    
    print len(finalDictionary)

if __name__ == '__main__':
    main()
    print "done"
