__author__ = 'Murugappan'
import codecs
from nltk.tokenize import word_tokenize

with codecs.open("train.txt","r","utf-8") as f:
    line=f.readlines()

for tweet in line:
    str=tweet.split("\t")
    print(word_tokenize(str[1]))
