import nltk
import re
import codecs

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


#Build Char Trigram vocabulary for forming features. Space is considered in trigrams. IS it fine ?
def charTrigramVoca(filename):
	chTriVoca = {}
	f = codecs.open(filename,'r',encoding='utf8')
	#f = io.open(filename,'r',encoding='utf8')
	line = f.readline()
	while line:
	    entr = re.split(r'\t+', line)
	    sentence = entr[0]
	    sentence = u"@#" + entr[0] + u"$%"
	    for i in range(2, len(sentence)):
	    	#print repr(sentence[i-2:i+1])
	    	addEntry(chTriVoca, sentence[i-2:i+1] )
	    line = f.readline()
	f.close()
	return chTriVoca

#Given a sentence(word) build the feature vector using chTriKeys
def charTrifeatureDict(word):
	chTriFea = {}
	word = "@#" + word + "$%"
	for key in chTriVocaKeys:
		chTriFea[key] = 1
	for i in range(2, len(word)):
		st = word[i-2:i+1]
		if st in chTriVocaKeys:
			updateKey(chTriFea, st, 1)
	return chTriFea



###Training and testing

# Return data should be used by apply features of NLTK to resolve memory error, But it is not working sometimes
# [(word, LangClass),....]
def buildLabelData(filename):
	f = codecs.open(filename,'r',encoding='utf8')
	line = f.readline()
	labelTrainData = []
	while line:
	    entr = re.split(r'\t+', line)
	    labelTrainData.append((entr[0], entr[1]))	
	    line = f.readline()
	f.close()
	return labelTrainData


def trainNaivebayes(trainFile, chGrams):
	labelTrainData = buildLabelData(trainFile)
	if chGrams == "uniGram":
		train_set = apply_features(charUnifeatureDict, labelTrainData)
	elif chGrams == "triGram":
		train_set = apply_features(charTrifeatureDict, labelTrainData)
	#import numpy as np
	#train_set = np.array(train_set)
	classifier = nltk.NaiveBayesClassifier.train(train_set)
	return classifier

def classifyTestData(filename, classifier, chGrams):
	labelTestData = buildLabelData(filename)
	if chGrams == "uniGram":
		test_set = apply_features(charUnifeatureDict, labelTestData)
	elif chGrams == "triGram":
		test_set = apply_features(charTrifeatureDict, labelTestData)

	#import numpy as np
	#test_set = np.array(test_set)
	accuracy = nltk.classify.accuracy(classifier, test_set)
	return accuracy

#Select the features from various trigrams in the vocabulary
def formFeaturesTri(chUniVoca):
	import operator
	selFea = sorted(chUniVoca.items(), key=operator.itemgetter(1), reverse = True)
	#print "\n\nSelFea"
	#print selFea
	chUniVocaKeys = []
	for item in selFea[20:500]:
		chUniVocaKeys.append(item[0])
	return chUniVocaKeys

from nltk.classify import apply_features
trainFile = "DSL_task_data-2016-04-06/DSL task data/training_data/DSLCC/train.txt"
testFile = "DSL_task_data-2016-04-06/DSL task data/training_data/DSLCC/devel.txt"
smallFile = "DSL_task_data-2016-04-06/DSL task data/training_data/DSLCC/small.txt"

chiUniVoca = {}
chiTriVoca = {}

def TriMain(trainFile, testfile):
	global chTriVoca
	chTriVoca = charTrigramVoca(testFile)
	#print chTriVoca

	chTriVocaKeys = formFeaturesTri(chTriVoca)
	#chTriVocaKeys = chTriVoca.keys()
	#print chTriVocaKeys
	#copyFiles(testFile, smallFile)
	
	classifier = trainNaivebayes(testFile, "triGram")
	accuracy = classifyTestData(testFile, classifier, "triGram")
	print "Accuracy of the classifier:"
	print accuracy