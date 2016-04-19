__author__ = 'Murugappan'

import codecs

output_train_files=["train_precision_oriented.txt","train_recall_oriented.txt","train_uniformly_sampled.txt"]

malaysian=[]
indonesian=[]
czech=[]
slovokian=[]
bosnian=[]
serbian=[]
for file in output_train_files:
    with codecs.open(file,"r","utf-8") as f:
        line=f.readline()
        while line:
            words=line.replace("\n","").split("\t")
            trigrams=[words[2][i:i+3] for i in range(len(words[2])-1)]
            if words[1]=='ms':
                malaysian.extend(trigrams)
            elif words[1]=='id':
                indonesian.extend(trigrams)
            elif words[1]=='cs':
                czech.extend(trigrams)
            elif words[1]=='sk':
                slovokian.extend(trigrams)
            elif words[1]=='bs':
                bosnian.extend(trigrams)
            elif words[1]=='sr':
                serbian.extend(trigrams)
            line=f.readline()

malaysian=list(set(malaysian))
indonesian=list(set(indonesian))
length=len(list(set(malaysian) & set(indonesian)))
similarity=float(length)/float(len(malaysian))

print("Unique trigrams in Mayasian is " + str(len(malaysian)))
print("Unique trigrams in Indonesian is " + str(len(indonesian)))
print("Common trigrams in Mayasian and Indonesian is " + str(length))
print("Similarity of malaysian with indonesian in % is "+str(similarity))

czech=list(set(czech))
slovokian=list(set(slovokian))
length=len(list(set(czech) & set(slovokian)))
similarity=float(length)/float(len(slovokian))

print("Unique trigrams in Czech is " + str(len(czech)))
print("Unique trigrams in Slovokian is " + str(len(slovokian)))
print("Common trigrams in Czech and Slovokian is " + str(length))
print("Similarity of malaysian with indonesian in % is "+str(similarity))

bosnian=list(set(bosnian))
serbian=list(set(serbian))
length=len(list(set(bosnian) & set(serbian)))
similarity=float(length)/float(len(serbian))

print("Unique trigrams in Bosnian is " + str(len(bosnian)))
print("Unique trigrams in Serbian is " + str(len(serbian)))
print("Common trigrams in Bosnian and Serbian is " + str(length))
print("Similarity of Bosnian with Serbian in % is "+str(similarity))