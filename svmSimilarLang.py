
##########SVM Sentence Classification for similar langauges########
'''
Date: 4/15/2016
Trying to write the classifier in general terms with many parameters (useful for comparative analysis)

Parameters:
character n - grams = 1, 2, 3, 4, 5, 6
Number of features from each language - NUMFEA (k)
'''
##Dictionary Functions
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
NGRAM = 3
SIMILARCLUSTER = u'Cluster10'		#10 81.55, 1 (0.8725), 5 (99.825), 46(1), 19(1), 18 (1)
CLASSIFIER = "SVM"
#CLASSIFIER = "NAIVEBAYES"



import time
import nltk
import re
import codecs
import pickle
from nltk.classify import apply_features

from nltk.classify import SklearnClassifier
from sklearn.svm import SVC


#adds st to the correspondong culster dictionary. In else case, it creates new dictionary for the cluster and then adds
def langAddEntry(diction, st, lang):
    if(diction.has_key(lang)):
        addEntry(diction[lang], st)
    else:
    	diction[lang] = {}
        addEntry(diction[lang], st)


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
	    if(entr[0] == SIMILARCLUSTER):
	    	for i in range(NGRAM - 1, len(sentence)):
	    		langAddEntry(chNgramVoca, sentence[i-(NGRAM - 1):i+1], entr[1] )
	    line = f.readline()
	f.close()
	return chNgramVoca

#Select top NUMFEA Ngrams from each langauge
def selectFeatures(chNgramVoca):
	langs = chNgramVoca.keys()
	features = set()
	import operator
	for lang in langs:
		selFea = sorted(chNgramVoca[lang].items(), key=operator.itemgetter(1), reverse = True)
		print lang
		print len(selFea)
		print selFea[:5]
		for item in selFea[LOW:NUMFEA]:
			features.add(item[0])
	print "Features size:"
	print len(features)
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
	    if(entr[0] == SIMILARCLUSTER):
		    labelTrainData.append((entr[2][:-1], entr[1]))	
	    line = f.readline()
	f.close()
	return labelTrainData

def trainNaivebayes(trainFile):
	labelTrainData = buildLabelData(trainFile)
	train_set = apply_features(charNgramfeatureDict, labelTrainData)
	if CLASSIFIER == "NAIVEBAYES":
		classifier = nltk.NaiveBayesClassifier.train(train_set)
	elif CLASSIFIER == "SVM":
		classifier = SklearnClassifier(SVC()).train(train_set)
	return classifier

def classifyTestData(filename, classifier):
	labelTestData = buildLabelData(filename)
	test_set = apply_features(charNgramfeatureDict, labelTestData)
	accuracy = nltk.classify.accuracy(classifier, test_set)
	return accuracy

def mytestClassifier(filename, classifier):
	outfile = "output/dsl/" + SIMILARCLUSTER + "_out.txt"
	wrongout = "output/dsl/" + SIMILARCLUSTER + "_wrongout.txt"
	fo = codecs.open(outfile, 'w', encoding = 'utf8')
	wo = codecs.open(wrongout, 'w', encoding = 'utf8')
	f = codecs.open(filename,'r',encoding='utf8')
	line = f.readline()
	count = 0
	correct = 0
	while line:
	    entr = re.split(r'\t+', line)
	    if(entr[0] == SIMILARCLUSTER):
	    	ans = classifier.classify(charNgramfeatureDict(entr[2][:-1]))
	    	#fo.write(ans + "\t" + entr[1] + "\n")
	    	count += 1
	    	#print repr(ans + "::" + entr[1])
	    	if ans == entr[1]:
	    		fo.write(ans + "\t" + entr[1] + "\n")
	    		correct += 1
	    	else:
	    		wo.write(ans + "\t" + entr[1] + "\t" + entr[2])
	    line = f.readline()
	f.close()
	fo.close()
	wo.close()
	return (correct/float(count))


trainFile = "C:/Users/gsr/Desktop/NLP Project/code/data/dsl/dsl_formatted_training.txt"
testFile = "C:/Users/gsr/Desktop/NLP Project/code/data/dsl/development_DSL.txt"
smallFile = "C:/Users/gsr/Desktop/NLP Project/code/data/dsl/small.txt"
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

	'''save_classifier(classifier)

	#classifier2 = load_classifier()

	print "Testing on file:"+ testFile
	accuracy = classifyTestData(testFile, classifier)
	print "Accuracy of the classifier:"
	print accuracy
	cend = time.time()
	print(cend - tend)'''

	accuracy = mytestClassifier(testFile, classifier)
	print "Accuracy of the classifier:"
	print accuracy
	cend = time.time()
	print "Time taken for classification:"
	print(cend - tend)

