import sys
import os
import codecs

test_file = sys.argv[1]

fin = codecs.open(test_file,"r","utf-8")
TP = 0
FP = 0
FN = 0
for line in fin.readlines():
    lists = line.split()
    if len(lists) < 2:
        continue
    if lists[-1]=="B" and lists[-2]=="B":
        TP += 1
    elif lists[-1]=="B" and lists[-2]!="B":
        FP += 1
    elif lists[-1]!="B" and lists[-2]=="B":
        FN += 1

precision = float(TP) / float(TP+FP)
recall = float(TP) / float(TP+FN)
F = 2 * precision * recall / (precision + recall)
print("P:"+str(precision)+"\tR:"+str(recall)+"\tF:"+str(F))
