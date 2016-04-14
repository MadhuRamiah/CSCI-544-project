# encoding: utf-8
__author__ = 'Murugappan'

import re
import codecs

data=[]
language_dict=dict()
language_list=[]
language_full={}
id={}
cluster_name={}
with codecs.open("precision.json","r","utf-8") as f:
    lines = f.readlines() # read only the first tweet/line

with codecs.open("precision_oriented.tsv","r","utf-8") as f:
    tsv=f.readlines()

with open("cluster.txt","r") as f:
    clusters=f.readlines()

language_id=[]
language_value=[]
cluster_id=[]
for cluster in clusters:
    print(cluster)
    str=cluster.replace("\n","")
    str=str.split("   ")
    cluster_name[str[1]]=str[0]
    #cluster_id.append(str[1])

for line in tsv:
    language=line.replace("\n","").split("\t")
    language_id.append(language[1])
    language_full[language[1]]=language[0]
    if language[0] not in language_list:
        language_list.append(language[0])
        language_dict[language[0]]=[]


i=0
del lines[-1]
for line in lines:
    #print(line)
    formatted=line.split(",",1)
    #print(formatted)
    formatted[0]=formatted[0][2:-1]
    if len(formatted[1])>2:
        formatted[1]=formatted[1][:-2]
        id[formatted[0]]=formatted[1]
    language_dict[language_full[formatted[0]]].append(formatted[1])
    i=i+1

items=[]
with codecs.open("train_precision_oriented.txt","w","utf-8") as f:
    f_test=codecs.open("test_precision_oriented.txt","w","utf-8")
    for item in language_dict:
        value=language_dict[item]
        length=len(value)
        train=int(0.8*length)
        if train==0 and length>0:
            train=1
        print(train)
        print(length-train)
        print(length)
        print("-----------------------------------------------")
        test=length-train
        for i in range(0,train):
            items.append(item)
            text = re.sub(r"http\S+", "", value[i])
            f.write(cluster_name[item]+"\t"+item+"\t"+text+"\n")
        for i in range(train,length):
            items.append(item)
            text = re.sub(r"http\S+", "", value[i])
            f_test.write(cluster_name[item]+"\t"+item+"\t"+text+"\n")
f.close()

#print(list(set(items)-set(cluster_id)))