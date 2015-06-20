'''
Gets the frequencies of all the words in the dictionary for each document in the corpus
'''
from __future__ import division
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import os
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
import csv
from decimal import Decimal
from math import log, fabs

dictionary = set()

#processes the text in all the documents so that the analysis can be completed
def getDocText(full_stop_set,filename ):
    
    #open and read the file
    raw = open(filename).read()

    #first pass on the words. creates a token based on spaces in the text, converts to lower case and removes anything in the stop set (words, chars, unicode, etc..)
    #this step is necessary to preprocess the text so nltk does not crash
    file_words = [w.lower() for w in raw.split()]
    
    filtered_file_words = [w for w in file_words if w not in full_stop_set]
    
    #recombines the text and passes to ntlk to do a proper tokenize
    tokens = word_tokenize(str(filtered_file_words).rstrip())
    
    #during the rsplit process above, it inserts a ' char, this removes it
    t = [x.replace("'", "") for x in tokens]
    
    #removes a lot more words with unicode chars in the middle of the word, and words with chars that aren't needed in the dictionary
    t_final = [(x.lower()) for x in t if (x not in full_stop_set) and (len(x) > 2) and (x.find('\\x') == -1) and (x.find('/') == -1) and (x.find('\\') == -1) and (x.find('.') == -1) and (x.find('*') != 0) and (x.find('-') != 0)and (x.find('+') != 0 and (x.find(':') == -1))]
    text = []
    [text.append(x.encode('utf-8')) for x in t_final ]
    
    #print "full stop set...", full_stop_set
   
   
    lemmList = []
    for t in text:
        if t not in full_stop_set:
            newWord = removePostFix(t)
            if t not in full_stop_set:
                lemmList.append(newWord)
    
    #wnl = nltk.WordNetLemmatizer()
    #for t in text:
    #    lemT = wnl.lemmatize(t)
    #    if lemT not in full_stop_set:
    #        lemmList.append(lemT)
        
    return sorted(lemmList)


def getFrequency(dictionary, wordsInDoc_List):
    
     
    freq = {}
    
    #for word in set(wordsInDoc_List):
    #    if word in dictionary:
    #        freq[word] = 0
            
    wordsBeingCounted = [word for word in wordsInDoc_List if word in dictionary]
    
    #print "length of frequency...", len(freq)
    
    
    freq = dict.fromkeys(set(wordsBeingCounted), 0)
    
    #assert(len(freq) == len(set(wordsInDoc_List)))
    #print sorted(freq.keys())
    
    
    for w in wordsBeingCounted:
        if freq.has_key(w):         
            freq[w] += 1
            #print word, freq[w]
        
    for f in freq.keys():
        frequency = freq[f]/len(wordsBeingCounted)
        freq[f] = frequency
    
    totalSum = 0
    for f in freq.keys():
        totalSum += freq[f]

    print "Sum of Frequencies: ", totalSum
    
    return freq



def writetofile(script_dir, freq, filename):
    #write to csv file
    with open(script_dir + 'WordFreq3.csv', 'a') as f:
        writer = csv.writer(f)
        for k,v in sorted(freq.items()):
            writer.writerow([k, v, filename])
            
    f.close()
        
    
def readDictionary(path):
    d = set()
    with open(path+'lemmDictionary_full3.txt', 'rU') as f:
        for word in f:
            d.add(word.strip())
    
    f.close()
    return sorted(d)

def removePostFix(argWord):
    leaves = ["s", "es", "ed", "er", "ly", "ing"]
    
    for leaf in leaves:
        if argWord[-len(leaf):] == leaf:
            return argWord[:-len(leaf)]
        else:
            return argWord

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
    full_stop_set = sorted(set(nltk.corpus.stopwords.words('english')) | punctuation | unicode_chars | other_words | stop_words | ingorelist_words)
    
    #print full_stop_set
    
    dictionary = readDictionary(dicionary_path)
    
    
    totalLength = 0
    path = file_path+"Company/"
    for filename in os.listdir(path):
        print "\nworking on ", filename
        #hidden file in osx filesytems. if it's present in the directory, then it skips the file
        if filename == ".DS_Store":
            continue
        
        wordsInDoc_List = getDocText(full_stop_set,path+filename)
        #wordsInDoc_Set = set(wordsInDoc_List)
        
        
        #totalWordsInDoc = len(wordsInDoc_Set)
        
        
        print 'words in list:', len(wordsInDoc_List)
        #print 'words in set: ' , totalWordsInDoc
        #print "difference: ", len(wordsInDoc_List) - totalWordsInDoc
        
                
        #get count of all words in the document
        freq = {}   
        freq = getFrequency(dictionary,wordsInDoc_List)
        
        #for k,v in sorted(freq.items()):
        #    print k,v
        
        writetofile(script_dir, freq, filename)
        totalLength += len(freq)
    
    print totalLength

if __name__ == '__main__':
    main()
    print "done"
