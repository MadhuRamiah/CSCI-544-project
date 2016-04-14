# encoding: utf-8
__author__ = 'Murugappan'

import json
import codecs

data=[]
language_dict=dict()
language_list=[]
language_full={}
id={}
cluster_name={}
with codecs.open("uniformly_sampled.json","r","utf-8") as f:
    lines = f.readlines() # read only the first tweet/line

with codecs.open("uniformly_sampled.tsv","r","utf-8") as f:
    tsv=f.readlines()

with open("cluster.txt","r") as f:
    clusters=f.readlines()

language_id=[]
language_value=[]
cluster_id=[]
for cluster in clusters:
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
with codecs.open("train_uniformly_sampled.txt","w","utf-8") as f:
    for item in language_dict:
        value=language_dict[item]
        for val in value:
            items.append(item)
            f.write(cluster_name[item]+"\t"+item+"\t"+val+"\n")
f.close()

#print(list(set(items)-set(cluster_id)))