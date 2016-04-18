from __future__ import absolute_import

from __future__ import unicode_literals

from nltk.tag.api import TaggerI

from nltk.tag import CRFTagger

import pycrfsuite

import unicodedata

import re

import codecs

train_data=[]
with codecs.open("nepali-english-demo-80%training-data.txt","r","utf-8") as f:
    line=f.readline()
    line_list=[]
    while line:
        #print(line)
        words=line.replace("\r","").replace("\n","").split("\t")
        #print(words)
        if(len(words)<2):
            train_data.append(line_list)
            line_list=[]
        else:
            tup1=(words[0],words[1])
            line_list.append(tup1)
        line=f.readline()
    f.close()
ct = CRFTagger()
#train_data = [[('University','Noun'), ('is','Verb'), ('a','Det'), ('good','Adj'), ('place','Noun')],[('dog','Noun'),('eat','Verb'),('meat','Noun')]]

ct.train(train_data,'model.crf.tagger')

test_actual=[]
test_sentences=[]
with codecs.open("nepali-english-demo-20%training-data.txt","r","utf-8") as f:
    line=f.readline()
    test=[]
    sentence=[]
    while line:
        words=line.replace("\r","").replace("\n","").split("\t")
        #print(words)
        if(len(words)<2):
            test_actual.append(test)
            test_sentences.append(sentence)
            test=[]
            sentence=[]
        else:
            tup1=(words[0],words[1])
            sentence.append(words[0])
            test.append(tup1)
        line=f.readline()
    f.close()

#ct.tag_sents([['dog','is','good'], ['Cat','eat','meat']])
ct.tag_sents(test_sentences)

#[[('dog', 'Noun'), ('is', 'Verb'), ('good', 'Adj')], [('Cat', 'Noun'), ('eat', 'Verb'), ('meat', 'Noun')]]
#gold_sentences = [[('dog','Noun'),('is','Verb'),('good','Adj')] , [('Cat','Noun'),('eat','Verb'), ('meat','Noun')]]

gold_sentences=test_actual
a = ct.evaluate(gold_sentences)

print(a)
