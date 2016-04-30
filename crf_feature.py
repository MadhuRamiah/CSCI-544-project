from __future__ import absolute_import
from __future__ import unicode_literals
import unicodedata
import re 
from nltk.tag.api import TaggerI
from nltk.tag import CRFTagger
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score,f1_score
import codecs
import nltk.metrics.scores
try:
    import pycrfsuite
except ImportError:
    pass

class CRFTagger(TaggerI):
    """
    A module for POS tagging using CRFSuite https://pypi.python.org/pypi/python-crfsuite
    
    >>> from nltk.tag import CRFTagger
    >>> ct = CRFTagger()
 
    >>> train_data = [[('University','Noun'), ('is','Verb'), ('a','Det'), ('good','Adj'), ('place','Noun')],
    ... [('dog','Noun'),('eat','Verb'),('meat','Noun')]]
    
    >>> ct.train(train_data,'model.crf.tagger')
    >>> ct.tag_sents([['dog','is','good'], ['Cat','eat','meat']])
    [[('dog', 'Noun'), ('is', 'Verb'), ('good', 'Adj')], [('Cat', 'Noun'), ('eat', 'Verb'), ('meat', 'Noun')]]
    
    >>> gold_sentences = [[('dog','Noun'),('is','Verb'),('good','Adj')] , [('Cat','Noun'),('eat','Verb'), ('meat','Noun')]] 
    >>> ct.evaluate(gold_sentences) 
    1.0
    
    Setting learned model file  
    >>> ct = CRFTagger() 
    >>> ct.set_model_file('model.crf.tagger')
    >>> ct.evaluate(gold_sentences)
    1.0
    
    """
    
    
    def __init__(self,  feature_func = None, verbose = False, training_opt = {}):
        """
        Initialize the CRFSuite tagger 
        :param feature_func: The function that extracts features for each token of a sentence. This function should take 
        2 parameters: tokens and index which extract features at index position from tokens list. See the build in 
        _get_features function for more detail.   
        :param verbose: output the debugging messages during training.
        :type verbose: boolean  
        :param training_opt: python-crfsuite training options
        :type training_opt : dictionary 
        
        Set of possible training options (using LBFGS training algorithm).  
         'feature.minfreq' : The minimum frequency of features.
         'feature.possible_states' : Force to generate possible state features.
         'feature.possible_transitions' : Force to generate possible transition features.
         'c1' : Coefficient for L1 regularization.
         'c2' : Coefficient for L2 regularization.
         'max_iterations' : The maximum number of iterations for L-BFGS optimization.
         'num_memories' : The number of limited memories for approximating the inverse hessian matrix.
         'epsilon' : Epsilon for testing the convergence of the objective.
         'period' : The duration of iterations to test the stopping criterion.
         'delta' : The threshold for the stopping criterion; an L-BFGS iteration stops when the
                    improvement of the log likelihood over the last ${period} iterations is no greater than this threshold.
         'linesearch' : The line search algorithm used in L-BFGS updates:
                           { 'MoreThuente': More and Thuente's method,
                              'Backtracking': Backtracking method with regular Wolfe condition,
                              'StrongBacktracking': Backtracking method with strong Wolfe condition
                           } 
         'max_linesearch' :  The maximum number of trials for the line search algorithm.
         
        """
        self._model_file = ''
        self._tagger = pycrfsuite.Tagger()
        
        if feature_func is None:
            self._feature_func =  self._get_features
        else:
            self._feature_func =  feature_func
        
        self._verbose = verbose 
        self._training_options = training_opt
        self._pattern = re.compile(r'\d')
        
    def set_model_file(self, model_file):
        self._model_file = model_file
        self._tagger.open(self._model_file)
    

    def _get_features(self, sent, i,tags):
	#print sent[i]
	features_list= []
	if not sent[i]:
            return features_list
	 	
	word = sent[i][0]
	index = str(i)
	if len(sent[i]) > 1:
    		postag = sent[i][1]
	else:
		postag = ""
    	features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    	]

	#Position
        features.append('POSITION='+index)
 
	# Emoticons
	match = re.match(r'(?:[:=;][oO\-]?[D\)\]\(\]/\\OpP])',sent[i])
        if match:
           features.append('EMOTICON')

	 # Punctuation
        punc_cat = set(["Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"])
        if all (unicodedata.category(x) in punc_cat for x in sent[i]):
            features.append('PUNCTUATION')

        #SYMBOLS
        sym_cat = set(["Sc", "Sk", "Sm", "So"])
        if all (unicodedata.category(x) in sym_cat for x in sent[i]):
            features.append('SYMBOLS')
    	
	if i > 0 and sent[i-1]:
		index = str(i-1)
        	word1 = sent[i-1][0]
		if len(sent[i-1]) > 1:
                	postag1 = sent[i-1][1]
        	else:
                	postag1 = ""
        	#postag1 = sent[i-1][1]
        	features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        	])
		#features.append('-1:POSITION='+index)
    	else:
        	features.append('BOS')
        
    	if i < len(sent)-1 and sent[i+1]:
		index = str(i+1)
        	word1 = sent[i+1][0]
		if len(sent[i+1]) > 1:
                        postag1 = sent[i+1][1]
                else:
                        postag1 = ""
        	#postag1 = sent[i+1][1]
        	features.extend([
            	'+1:word.lower=' + word1.lower(),
            	'+1:word.istitle=%s' % word1.istitle(),
            	'+1:word.isupper=%s' % word1.isupper(),
            	'+1:postag=' + postag1,
            	'+1:postag[:2]=' + postag1[:2],
        	])
		#features.append('+1:POSITION='+index)
    	else:
        	features.append('EOS')
	if len(sent[i]) > 1:
            features.append('SUF_' + sent[i][-1:])
        if len(sent[i]) > 2:
            features.append('SUF_' + sent[i][-2:])
        if len(sent[i]) > 3:
            features.append('SUF_' + sent[i][-3:])
        	
    	return features	

       
    """
    def _get_features(self, tokens, idx,tags):

        Extract basic features about this word including 
             - Current Word 
             - Is Capitalized ?
             - Has Punctuation ?
             - Has Number ?
             - Suffixes up to length 3
        Note that : we might include feature over previous word, next word ect. 
        
        :return : a list which contains the features
        :rtype : list(str)    
        
	#print "hi inside get features"
        #print tokens,idx 
        token = tokens[idx]
        
        feature_list = []
        
        if not token:
            return feature_list
            
        # Capitalization 
        if token[0].isupper():
            feature_list.append('CAPITALIZATION')
            #feature_list.append('ne')
        
        # Number 
        if re.search(self._pattern, token) is not None:
            feature_list.append('HAS_NUM') 
        
        # Punctuation
        punc_cat = set(["Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"])
        if all (unicodedata.category(x) in punc_cat for x in token):
            feature_list.append('PUNCTUATION')
        
	#SYMBOLS
	sym_cat = set(["Sc", "Sk", "Sm", "So"])
        if all (unicodedata.category(x) in sym_cat for x in token):
            feature_list.append('SYMBOLS')

        # Suffix up to length 3
        if len(token) > 1:
            feature_list.append('SUF_' + token[-1:]) 
        if len(token) > 2: 
            feature_list.append('SUF_' + token[-2:])    
        if len(token) > 3: 
            feature_list.append('SUF_' + token[-3:])
        

	#print tags
	if len(tags)>0:
		feature_list.append('PREF_'+tokens[idx-1])
		#feature_list.append('PREF_'+tags[idx-1])
	if len(tags)>1:
		#feature_list.append('PREF_'+tokens[idx-2])
		feature_list.append('PREF_'+tokens[idx-1])
	if len(tokens)-idx-1>0:
		feature_list.append('SUF_'+tags[idx+1])
	if len(tokens)-idx-1>1:
                feature_list.append('SUF_'+tags[idx+1])
		#feature_list.append('SUF_'+tags[idx+2])
        feature_list.append('WORD_' + token )
        
        return feature_list
    """




        
    def tag_sents(self, sents):
        '''
        Tag a list of sentences. NB before using this function, user should specify the mode_file either by 
                       - Train a new model using ``train'' function 
                       - Use the pre-trained model which is set via ``set_model_file'' function  
        :params sentences : list of sentences needed to tag. 
        :type sentences : list(list(str))
        :return : list of tagged sentences. 
        :rtype : list (list (tuple(str,str))) 
        '''
        if self._model_file == '':
            raise Exception(' No model file is found !! Please use train or set_model_file function')
        
        # We need the list of sentences instead of the list generator for matching the input and output
        result = []
	labels=[]  
        for tokens in sents:
            features = [self._feature_func(tokens,i,labels) for i in range(len(tokens))]
	    labels = self._tagger.tag(features)
            #label_total.append(labels)
            #print "f****"+str(features)i
	    #print "l*****"+str(labels)
            if len(labels) != len(tokens):
                raise Exception(' Predicted Length Not Matched, Expect Errors !')
            
            tagged_sent = list(zip(tokens,labels))
            #print tagged_sent
	    result.append(tagged_sent)
            
        return result 
    
    def train(self, train_data, model_file):
        '''
        Train the CRF tagger using CRFSuite  
        :params train_data : is the list of annotated sentences.        
        :type train_data : list (list(tuple(str,str)))
        :params model_file : the model will be saved to this file.     
         
        '''
        trainer = pycrfsuite.Trainer(verbose=self._verbose)
        trainer.set_params(self._training_options)
        
        for sent in train_data:
            tokens,labels = zip(*sent)
            features = [self._feature_func(tokens,i,labels)for i in range(len(tokens))]
            trainer.append(features,labels)
                        
        # Now train the model, the output should be model_file
	"""trainer.set_params({
  	  #'c1': 3.0,   # coefficient for L1 penalty
    	#'c2': 3.0,  # coefficient for L2 penalty
    	'max_iterations': 100,  # stop earlier

    	# include transitions that are possible, but not observed
    	'feature.possible_transitions': True
	})"""

        trainer.train(model_file)
        # Save the model file
        self.set_model_file(model_file) 

    def tag(self, tokens):
        '''
        Tag a sentence using Python CRFSuite Tagger. NB before using this function, user should specify the mode_file either by 
                       - Train a new model using ``train'' function 
                       - Use the pre-trained model which is set via ``set_model_file'' function  
        :params tokens : list of tokens needed to tag. 
        :type tokens : list(str)
        :return : list of tagged tokens. 
        :rtype : list (tuple(str,str)) 
        '''
	#print "****************"+str(tokens)        
        return self.tag_sents([tokens])[0]


"""ct = CRFTagger()

train_data = [[('University','Noun'), ('is','Verb'), ('a','Det'), ('good','Adj'), ('place','Noun')],
[('dog','Noun'),('eat','Verb'),('meat','Noun')]]

ct.train(train_data,'model.crf.tagger')
ct.tag_sents([['dog','is','good'], ['Cat','eat','meat']])
gold_sentences = [[('dog','Noun'),('is','Verb'),('good','Adj')] , [('Cat','Noun'),('eat','Verb'), ('meat','Noun')]]
result = ct.evaluate(gold_sentences)
print result 
"""

train_data=[]
#with codecs.open("nepali-english-demo-80%training-data.txt","r","utf-8") as f:
with codecs.open("/Users/Preethi/nlp_project/EMNLP/spanish_english/training/spanish-english-training-80%.txt","r","utf-8") as f:
#with codecs.open("/Users/Preethi/nlp_project/EMNLP/mandarin_english/training/mandarin-english-training.txt","r","utf-8") as f:
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

ct.train(train_data,'model.crf.tagger')


test_actual=[]
test_sentences=[]
#with codecs.open("nepali-english-demo-20%training-data.txt","r","utf-8") as f:
with codecs.open("/Users/Preethi/nlp_project/EMNLP/spanish_english/training/spanish-english-training-20%.txt","r","utf-8") as f:
#with codecs.open("/Users/Preethi/nlp_project/EMNLP/mandarin_english/training/mandarin-english-testing-answers.txt","r","utf-8") as f:
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

res = ct.tag_sents(test_sentences)
tagged_result = []
tagged_actual = []
for i in range(len(res)):
   for j in range(len(res[i])):
	tagged_result.append(res[i][j][1])
	tagged_actual.append(test_actual[i][j][1])
print res[0]
print test_actual[0]
#print tagged_result[0]
#print tagged_actual[0]

gold_sentences=test_actual
accuracy = ct.evaluate(gold_sentences)
print "accuracy:"+str(accuracy)

#recall = nltk.metrics.scores.recall(test_actual,res)
precision = precision_score(tagged_actual,tagged_result)
print "precision:"+str(precision)

recall = recall_score(tagged_actual,tagged_result)
print "recall:"+str(recall)


f1 = f1_score(tagged_actual,tagged_result)
print "F1_score:"+str(f1)

