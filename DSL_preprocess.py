import sys
input = open("train.txt","r")

output = open("dsl_formatted.txt", "w")

line = input.readline().strip("\n")
i = 0
while len(line.strip()) != 0:
    arr = line.split("\t")
    if len(arr) == 3:
        cluster = arr[1]
        language = arr[2]
        data = arr[0]
        if(cluster == "A"):
            cluster = "Cluster10"
        elif cluster == "B":
            cluster = "Cluster1"
            if language == "my":
                language = "ms"
        elif cluster == "C":
            cluster = "Cluster5"
            if language == "cz":
                language = "cs"
        elif cluster == "D":
            cluster = "Cluster46"
            language = "pt"

        elif cluster == "E":
            cluster = "Cluster19"
            language = "es"

        elif cluster == "F":
            cluster = "Cluster18"
            language = "en"
        output.write(cluster+"\t"+language+"\t"+data+"\n")
    line = input.readline().strip("\n")

    i+=1
