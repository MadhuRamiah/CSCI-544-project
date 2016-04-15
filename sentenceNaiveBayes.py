##########Naive Bayes Sentence Classification########
'''
Date: 4/14/2016
Trying to write the classifier in general terms with many parameters (useful for comparative analysis)

Fix from prev Sentence classifiers: 
Planning to use top NUMFEA frequent ngrams from each langauge.
Previosuly we used top k features from entire dataset.

Parameters:
character n - grams = 1, 2, 3, 4, 5, 6
Number of features from each language - NUMFEA (k)
'''
##Dictionary Functions
#Not Working
def printDict(diction):
	keys = diction.keys()
	print keys
	for i in range(0, len(keys)):
		print keys[i]

def addKey(diction, key):
    diction[key] = 1
def updateKey(diction, key, value):
    diction[key] = diction[key] + value
 
def addEntry(diction, st):
    if(diction.has_key(st)):
        updateKey(diction, st, 1)
    else:
        addKey(diction, st)


LOW = 0
NUMFEA = 1000
NGRAM = 4

import time
import nltk
import re
import codecs
from nltk.classify import apply_features
#adds st to the correspondong culster dictionary. In else case, it creates new dictionary for the cluster and then adds
def langAddEntry(diction, st, cluster):
    if(diction.has_key(cluster)):
        addEntry(diction[cluster], st)
    else:
    	diction[cluster] = {}
        addEntry(diction[cluster], st)


#Given a sentence(or word) build the feature vector using selected features set
def charNgramfeatureDict(word):
	chNgramFea = {}
	#word = "@#" + word + "$%"
	for key in features:
		chNgramFea[key] = 1
	for i in range(NGRAM - 1, len(word)):
		st = word[i-(NGRAM - 1):i+1]
		if st in features:
			updateKey(chNgramFea, st, 1)
	return chNgramFea




#Build Char Ngrams vocabulary for forming features. Space is considered in Ngrams. Builds dictionary for each langauge cluster
def charNgramVoca(filename):
	chNgramVoca = {}
	f = codecs.open(filename,'r',encoding='utf8')
	#f = io.open(filename,'r',encoding='utf8')
	line = f.readline()
	while line:
	    entr = re.split(r'\t+', line)
	    sentence = entr[2][:-1]
	    #print repr(sentence)
	    #sentence = u"@#" + entr[2] + u"$%"
	    for i in range(NGRAM - 1, len(sentence)):
	    	langAddEntry(chNgramVoca, sentence[i-(NGRAM - 1):i+1], entr[0] )
	    line = f.readline()
	f.close()
	return chNgramVoca

#Select top NUMFEA Ngrams from each cluster
def selectFeatures(chNgramVoca):
	clusters = chNgramVoca.keys()
	features = set()
	import operator
	for cluster in clusters:
		selFea = sorted(chNgramVoca[cluster].items(), key=operator.itemgetter(1), reverse = True)
		#print selFea
		for item in selFea[LOW:NUMFEA]:
			features.add(item[0])
	return features


###Training and testing

# Return data should be used by apply features of NLTK to resolve memory error, But it is not working sometimes
# [(word, LangClass),....]
def buildLabelData(filename):
	f = codecs.open(filename,'r',encoding='utf8')
	line = f.readline()
	labelTrainData = []
	while line:
	    entr = re.split(r'\t+', line)
	    labelTrainData.append((entr[2], entr[0]))	
	    line = f.readline()
	f.close()
	return labelTrainData

def trainNaivebayes(trainFile):
	labelTrainData = buildLabelData(trainFile)
	train_set = apply_features(charNgramfeatureDict, labelTrainData)
	classifier = nltk.NaiveBayesClassifier.train(train_set)
	return classifier

def classifyTestData(filename, classifier):
	labelTestData = buildLabelData(filename)
	test_set = apply_features(charNgramfeatureDict, labelTestData)
	accuracy = nltk.classify.accuracy(classifier, test_set)
	return accuracy

trainFile = "C:/Users/gsr/Desktop/NLP Project/code/data/twitter/train_recall_oriented.txt"
testFile = "C:/Users/gsr/Desktop/NLP Project/code/data/twitter/test_recall_oriented.txt"
smallFile = "C:/Users/gsr/Desktop/NLP Project/code/data/twitter/small.txt"
features = set()	#needs to be global because charNgramfeatureDict doesn't accept more than one argument


def NgramMain(trainFile, testFile):
	chNgramVoca = charNgramVoca(trainFile)
	#print chTriVoca
	global features
	features = selectFeatures(chNgramVoca)

	print "Training on file:"+ trainFile
	tstart = time.time()
	classifier = trainNaivebayes(trainFile)
	tend = time.time()
	print(tend - tstart)


	print "Testing on file:"+ testFile
	accuracy = classifyTestData(testFile, classifier)
	print "Accuracy of the classifier:"
	print accuracy
	cend = time.time()
	print(cend - tend)

