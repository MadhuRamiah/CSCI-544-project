#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import binascii
import codecs

input = open("nepali-english-20%training-data.txt","r")
file_pointer = open("nepali-english-final-training-data.tsv","r")
#output = open("temp.txt","w")

tweet = {}
previous_tweetid = ""
for line in input:
    arr = line.split("\t")
    if len(arr) == 3:
        id = str(arr[0])
        text = str(arr[2])

        if text != "Not Found\n":
            tweet[id] = text

with codecs.open("nepali-english-demo-20%training-data.txt","w","utf-8") as f:
    for passes in file_pointer:
        arr_split = passes.split("\t")
        #print (arr_split)
        if len(arr_split) == 5:
            tweet_id =  str(arr_split[0]).strip()
            start = int(arr_split[2].strip())
            #print start
            end = int(arr_split[3].strip())+1
            lang = str(arr_split[4]).strip("\n")
            if lang == "lang1":
                lang = "english"

            if lang == "lang2":
                lang = "nepali"


            if tweet_id in tweet:
                actual_tweet = tweet[tweet_id].decode('utf-8')
                string1 = actual_tweet[start:end]
		if tweet_id != previous_tweetid:
		   f.write("\n")
                f.write(string1+"\t"+lang+"\n")
                previous_tweetid = tweet_id
                

			






