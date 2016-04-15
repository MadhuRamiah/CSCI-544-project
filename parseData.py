# encoding: utf-8
__author__ = 'Murugappan'

import re
import codecs

#regex for preprocessing
regex_str = [
    r'(?:[:=;][oO\-]?[D\)\]\(\]/\\OpP])',
    r'<[^>]+>', # HTML tags
    r'@[.]*[/]*[ ]*[,]*', # @-mentions
    r'@[\w_]+', #@ removal
    r"http\S+", # http removal
    r"#[0-9]*",  #hash tag and number
    r"(?:\#+[0-9]*[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    ]

#function to remove unnecessary tags and urls
def regex(data):
    for reg in regex_str:
        data = re.sub(reg, "", data)
    return data


data=[]
language_dict=dict()
language_list=[]
language_full={}
id={}
cluster_name={}

#open the training files and read data
with codecs.open("recall.json","r","utf-8") as f:
    lines = f.readlines() # read only the first tweet/line

with codecs.open("recall_oriented.tsv","r","utf-8") as f:
    tsv=f.readlines()

with open("cluster.txt","r") as f:
    clusters=f.readlines()

#segregate into respective clusters
language_id=[]
language_value=[]
cluster_id=[]
for cluster in clusters:
    str=cluster.replace("\n","")
    str=str.split("   ")
    cluster_name[str[1]]=str[0]

#correlate tsv id's to json id's and extract tweet data
for line in tsv:
    language=line.replace("\n","").split("\t")
    language_id.append(language[1])
    language_full[language[1]]=language[0]
    if language[0] not in language_list:
        language_list.append(language[0])
        language_dict[language[0]]=[]

#remove the [] around the tweets
i=0
del lines[-1]
for line in lines:
    formatted=line.split(",",1)
    formatted[0]=formatted[0][2:-1]
    if len(formatted[1])>2:
        formatted[1]=formatted[1][:-2]
        id[formatted[0]]=formatted[1]
    language_dict[language_full[formatted[0]]].append(formatted[1])
    i=i+1

#write data in files
with codecs.open("train_recall_oriented.txt","w","utf-8") as f:
    f_test=codecs.open("test_recall_oriented.txt","w","utf-8")
    for item in language_dict:
        value=language_dict[item]
        length=len(value)
        train=int(0.8*length)                                       #train set is 80%
        if train==0 and length>0:
            train=1
        test=length-train                                           #test set is remaining 20%
        for i in range(0,train):
            text=regex(value[i])
            f.write(cluster_name[item]+"\t"+item+"\t"+text+"\n")    #write to train file
        for i in range(train,length):
            text=regex(value[i])
            f_test.write(cluster_name[item]+"\t"+item+"\t"+text+"\n")#write to test file
f.close()
